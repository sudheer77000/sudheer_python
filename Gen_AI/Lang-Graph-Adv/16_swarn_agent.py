
import operator
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal
from xml.sax.saxutils import escape

from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from rich.console import Console
from rich.panel import Panel
from rich.table import Table as RichTable
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.rule import Rule
from rich import box
from rich.markdown import Markdown

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table as PDFTable,
    TableStyle,
    HRFlowable,
)

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()



# ==========================================================
# 1. CONFIGURATION
# ==========================================================

console = Console()

AGENTS = [
    "flight",
    "hotel",
    "destination",
    "budget",
]

AGENT_STYLE = {
    "flight": "bright_cyan",
    "hotel": "bright_magenta",
    "destination": "bright_green",
    "budget": "bright_yellow",
}

AGENT_EMOJI = {
    "flight": "✈️",
    "hotel": "🏨",
    "destination": "🌍",
    "budget": "💰",
}

OUTPUT_DIR = Path("travel_reports")
PDF_FILE = OUTPUT_DIR / "Complete_Travel_Itinerary.pdf"


# ==========================================================
# 2. RICH HEADER
# ==========================================================

def show_header():

    console.print()

    console.print(
        Panel(
            "[bold white]TRAVEL PLANNER SWARM[/bold white]\n"
            "[cyan]Autonomous Multi-Agent Travel Planning[/cyan]\n\n"
            "[dim]Flight • Hotel • Destination • Budget[/dim]",
            border_style="bright_blue",
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )


# ==========================================================
# 3. OPENAI MODEL
# ==========================================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)


# ==========================================================
# 4. STRUCTURED AGENT DECISION
# ==========================================================

class AgentDecision(BaseModel):

    findings: str = Field(
        description="Useful findings from this specialist agent"
    )

    next_agent: Literal[
        "flight",
        "hotel",
        "destination",
        "budget",
        "finish",
    ] = Field(
        description="Which agent should receive control next"
    )

    reason: str = Field(
        description="Reason for selecting the next agent"
    )


decision_llm = llm.with_structured_output(AgentDecision)


# ==========================================================
# 5. SHARED LANGGRAPH STATE
# ==========================================================

class TravelState(TypedDict):

    request: str

    notes: Annotated[list[str], operator.add]

    visited_agents: Annotated[list[str], operator.add]

    next_agent: str

    steps: int

    final_answer: str


# ==========================================================
# 6. SPECIALIST AGENT PROMPTS
# ==========================================================

AGENT_PROMPTS = {

    "flight": """
You are an expert FLIGHT TRAVEL AGENT.

Analyze the user's travel request.

Responsibilities:
- Suggest suitable flight routes.
- Identify departure and arrival airports.
- Consider flight duration and layovers.
- Give flight booking advice.
- Consider the user's travel budget.

Do not invent live flight prices or availability.
Clearly label any prices as estimates.
""",

    "hotel": """
You are an expert HOTEL AGENT.

Responsibilities:
- Recommend suitable hotel areas.
- Suggest accommodation types.
- Consider hotel amenities and location.
- Consider the user's budget.
- Explain hotel selection criteria.

Do not invent live hotel availability.
""",

    "destination": """
You are an expert DESTINATION AGENT.

Responsibilities:
- Recommend popular attractions.
- Suggest local experiences.
- Create a practical daily itinerary.
- Recommend neighborhoods and activities.
- Consider interests and trip duration.
""",

    "budget": """
You are an expert TRAVEL BUDGET AGENT.

Responsibilities:
- Estimate flight expenses.
- Estimate hotel expenses.
- Estimate food expenses.
- Estimate local transportation.
- Estimate sightseeing expenses.
- Calculate the approximate total budget.

Clearly explain assumptions.
Do not present estimates as confirmed prices.
""",
}


# ==========================================================
# 7. DISPLAY AGENT RESULTS
# ==========================================================

def show_agent_activity(agent, findings, next_agent):

    color = AGENT_STYLE[agent]
    emoji = AGENT_EMOJI[agent]

    table = RichTable(
        show_header=False,
        box=box.ROUNDED,
        expand=True,
        padding=(0, 1),
    )

    table.add_column("Field", style="bold white", width=15)
    table.add_column("Details", style="white")

    table.add_row(
        "Agent",
        f"[{color}]{emoji} {agent.upper()}[/{color}]",
    )

    table.add_row(
        "Findings",
        findings,
    )

    table.add_row(
        "Next Handoff",
        f"[bold bright_blue]{next_agent.upper()}[/bold bright_blue]",
    )

    console.print(table)


# ==========================================================
# 8. CREATE SPECIALIST AGENTS
# ==========================================================

def create_agent(agent_name, progress, progress_task):

    def agent_node(state: TravelState):

        color = AGENT_STYLE[agent_name]
        emoji = AGENT_EMOJI[agent_name]

        console.print()

        console.print(
            Rule(
                f"[bold {color}]{emoji} "
                f"{agent_name.upper()} AGENT[/bold {color}]",
                style=color,
            )
        )

        previous_notes = "\n\n".join(state["notes"])

        available_agents = [
            agent
            for agent in AGENTS
            if agent not in state["visited_agents"]
            and agent != agent_name
        ]

        prompt = f"""
{AGENT_PROMPTS[agent_name]}

USER REQUEST:
{state["request"]}

PREVIOUS AGENT FINDINGS:
{previous_notes if previous_notes else "No previous findings."}

SPECIALISTS THAT HAVE NOT WORKED:
{available_agents}

INSTRUCTIONS:
1. Analyze the user's travel request.
2. Provide useful specialist findings.
3. Consider findings from previous agents.
4. Choose the next unvisited specialist.
5. Choose finish only when no other specialist is required.

Return structured output.
"""

        # Update the existing Rich progress display.
        # Do not use console.status() here because Progress
        # already owns the live terminal display.

        progress.update(
            progress_task,
            description=(
                f"[bold {color}]{emoji} "
                f"{agent_name.title()} agent is working..."
            ),
        )

        result = decision_llm.invoke(prompt)

        show_agent_activity(
            agent_name,
            result.findings,
            result.next_agent,
        )

        progress.advance(progress_task)

        return {
            "notes": [
                f"{agent_name.upper()} FINDINGS:\n"
                f"{result.findings}"
            ],

            "visited_agents": [agent_name],

            "next_agent": result.next_agent,

            "steps": state["steps"] + 1,
        }

    return agent_node


# ==========================================================
# 9. DYNAMIC SWARM ROUTER
# ==========================================================

def swarm_router(state: TravelState):

    remaining_agents = [
        agent
        for agent in AGENTS
        if agent not in state["visited_agents"]
    ]

    requested_agent = state["next_agent"]

    # All specialists must contribute before finalization.

    if not remaining_agents:

        console.print(
            "\n[bold green]✓ All specialist agents completed![/bold green]"
        )

        return "finalize"

    # Honor a valid handoff.

    if requested_agent in remaining_agents:

        next_agent = requested_agent

    else:

        # Prevent premature finish and repeated agents.

        next_agent = remaining_agents[0]

    console.print()

    console.print(
        "[bold bright_blue]⇢ SWARM HANDOFF[/bold bright_blue] "
        f"[white]{requested_agent.upper()}[/white] "
        "→ "
        f"[bold {AGENT_STYLE[next_agent]}]"
        f"{next_agent.upper()}[/bold {AGENT_STYLE[next_agent]}]"
    )

    return next_agent


# ==========================================================
# 10. FINAL TRAVEL COORDINATOR
# ==========================================================

def finalize_trip(state: TravelState):

    console.print()

    console.print(
        Rule(
            "[bold bright_green]FINAL TRAVEL COORDINATOR[/bold bright_green]"
        )
    )

    specialist_findings = "\n\n".join(state["notes"])

    prompt = f"""
You are the FINAL TRAVEL PLANNING COORDINATOR.

Combine all specialist findings into one professional
and practical travel itinerary.

USER REQUEST:
{state["request"]}

SPECIALIST FINDINGS:
{specialist_findings}

Create these sections:

# TRIP OVERVIEW

# FLIGHT RECOMMENDATIONS

# HOTEL RECOMMENDATIONS

# DAILY DESTINATION ITINERARY

# ESTIMATED TRAVEL BUDGET

# PRACTICAL TRAVEL TIPS

Use clear headings and bullet points.

Clearly distinguish estimates from confirmed information.
Do not claim live booking availability or verified prices.
"""

    console.print(
        "[bold green]Preparing final travel itinerary...[/bold green]"
    )

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }


# ==========================================================
# 11. BUILD LANGGRAPH SWARM
# ==========================================================

def build_swarm(progress, progress_task):

    graph = StateGraph(TravelState)

    # Register all specialist agents.

    for agent in AGENTS:

        graph.add_node(
            agent,
            create_agent(
                agent,
                progress,
                progress_task,
            ),
        )

    graph.add_node(
        "finalize",
        finalize_trip,
    )

    # Start with Flight Agent.

    graph.add_edge(
        START,
        "flight",
    )

    destinations = {
        "flight": "flight",
        "hotel": "hotel",
        "destination": "destination",
        "budget": "budget",
        "finalize": "finalize",
    }

    # Every agent can hand control to another agent.

    for agent in AGENTS:

        graph.add_conditional_edges(
            agent,
            swarm_router,
            destinations,
        )

    graph.add_edge(
        "finalize",
        END,
    )

    return graph.compile()


# ==========================================================
# 12. RICH FINAL RESULT
# ==========================================================

def display_final_result(state):

    console.print()

    console.print(
        Panel(
            Markdown(state["final_answer"]),
            title="[bold green]✈ YOUR TRAVEL ITINERARY[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )

    summary = RichTable(
        title="SWARM EXECUTION SUMMARY",
        box=box.ROUNDED,
        header_style="bold cyan",
        expand=True,
    )

    summary.add_column("Specialist Agent")
    summary.add_column("Execution Status", justify="center")

    for agent in AGENTS:

        summary.add_row(
            f"{AGENT_EMOJI[agent]} {agent.title()}",
            "[bold green]Completed ✓[/bold green]",
        )

    summary.add_row(
        "[bold]Total Agents[/bold]",
        f"[bold]{len(AGENTS)}[/bold]",
    )

    console.print(summary)


# ==========================================================
# 13. PDF GENERATION
# ==========================================================

def generate_travel_pdf(state):

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Always create one complete PDF.
    # The previous report is overwritten on the next run.

    doc = SimpleDocTemplate(
        str(PDF_FILE),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=22 * mm,
        title="Complete Travel Itinerary",
        author="Travel Planner Swarm",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="MainTitle",
            parent=styles["Title"],
            fontSize=22,
            leading=28,
            textColor=colors.HexColor("#174A7E"),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontSize=14,
            leading=19,
            textColor=colors.HexColor("#176B87"),
            spaceBefore=13,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="AgentHeading",
            parent=styles["Heading3"],
            fontSize=11,
            textColor=colors.HexColor("#174A7E"),
            spaceBefore=8,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            leftIndent=15,
            firstLineIndent=-9,
            spaceAfter=4,
        )
    )

    story = []

    # ------------------------------------------------------
    # PDF HEADER
    # ------------------------------------------------------

    story.append(Spacer(1, 15 * mm))

    story.append(
        Paragraph(
            "TRAVEL PLANNER",
            styles["MainTitle"],
        )
    )

    story.append(
        Paragraph(
            "Complete AI-Powered Travel Itinerary",
            styles["Subtitle"],
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=colors.HexColor("#176B87"),
        )
    )

    story.append(Spacer(1, 10))

    # ------------------------------------------------------
    # SECTION 1: USER REQUEST
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "1. TRAVEL REQUEST",
            styles["Section"],
        )
    )

    story.append(
        Paragraph(
            escape(state["request"]).replace("\n", "<br/>"),
            styles["BodyCustom"],
        )
    )

    # ------------------------------------------------------
    # SECTION 2: AGENT SUMMARY
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "2. SPECIALIST AGENT SUMMARY",
            styles["Section"],
        )
    )

    agent_data = [
        ["Specialist Agent", "Execution Status"],
        ["Flight Agent", "Completed"],
        ["Hotel Agent", "Completed"],
        ["Destination Agent", "Completed"],
        ["Budget Agent", "Completed"],
    ]

    agent_table = PDFTable(
        agent_data,
        colWidths=[80 * mm, 70 * mm],
        repeatRows=1,
    )

    agent_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#174A7E")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BACKGROUND", (0, 1), (-1, -1),
             colors.HexColor("#F1F5F9")),

            ("TEXTCOLOR", (0, 1), (-1, -1),
             colors.HexColor("#1E293B")),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),

            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(agent_table)

    # ------------------------------------------------------
    # SECTION 3: SPECIALIST FINDINGS
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "3. SPECIALIST FINDINGS",
            styles["Section"],
        )
    )

    for note in state["notes"]:

        heading, separator, content = note.partition("\n")

        story.append(
            Paragraph(
                escape(heading),
                styles["AgentHeading"],
            )
        )

        story.append(
            Paragraph(
                escape(content).replace("\n", "<br/>"),
                styles["BodyCustom"],
            )
        )

    # ------------------------------------------------------
    # SECTION 4: FINAL ITINERARY
    # ------------------------------------------------------

    story.append(
        Paragraph(
            "4. COMPLETE TRAVEL ITINERARY",
            styles["Section"],
        )
    )

    final_answer = state["final_answer"]

    for line in final_answer.splitlines():

        line = line.strip()

        if not line:

            story.append(Spacer(1, 4))
            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    escape(line[4:]),
                    styles["AgentHeading"],
                )
            )

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    escape(line[3:]),
                    styles["Section"],
                )
            )

        elif line.startswith("# "):

            story.append(
                Paragraph(
                    escape(line[2:]),
                    styles["Section"],
                )
            )

        elif line.startswith(("- ", "* ")):

            story.append(
                Paragraph(
                    "• " + escape(line[2:]),
                    styles["BulletCustom"],
                )
            )

        else:

            story.append(
                Paragraph(
                    escape(line),
                    styles["BodyCustom"],
                )
            )

    # ------------------------------------------------------
    # FOOTER AND PAGE NUMBERS
    # ------------------------------------------------------

    def add_footer(canvas, document):

        canvas.saveState()

        canvas.setStrokeColor(
            colors.HexColor("#CBD5E1")
        )

        canvas.line(
            20 * mm,
            15 * mm,
            A4[0] - 20 * mm,
            15 * mm,
        )

        canvas.setFont(
            "Helvetica",
            8,
        )

        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        canvas.drawString(
            20 * mm,
            10 * mm,
            "Generated by Travel Planner Swarm",
        )

        canvas.drawRightString(
            A4[0] - 20 * mm,
            10 * mm,
            f"Page {document.page}",
        )

        canvas.restoreState()

    # Build ONE complete multi-page PDF.

    doc.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )

    return PDF_FILE.resolve()


# ==========================================================
# 14. MAIN APPLICATION
# ==========================================================

def main():

    show_header()

    console.print(
        "\n[bold cyan]Tell me about your travel requirements.[/bold cyan]"
    )

    request = console.input(
        "\n[bold yellow]You → [/bold yellow]"
    )

    if not request.strip():

        console.print(
            "[bold red]Please enter a travel request.[/bold red]"
        )

        return

    console.print()

    console.print(
        Panel(
            request,
            title="[bold]YOUR TRAVEL REQUEST[/bold]",
            border_style="blue",
            padding=(1, 2),
        )
    )

    console.print()

    console.print(
        "[bold bright_blue]Starting autonomous travel swarm...[/bold bright_blue]"
    )

    # One Rich live display for the entire agent execution.

    with Progress(
        SpinnerColumn(style="bright_cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        refresh_per_second=8,
    ) as progress:

        task = progress.add_task(
            "Starting travel swarm...",
            total=len(AGENTS),
        )

        swarm = build_swarm(
            progress,
            task,
        )

        initial_state = {
            "request": request,
            "notes": [],
            "visited_agents": [],
            "next_agent": "flight",
            "steps": 0,
            "final_answer": "",
        }

        # Execute all agents and final coordinator.

        result = swarm.invoke(initial_state)

        progress.update(
            task,
            description="[bold green]All agents completed![/bold green]",
        )

    # ------------------------------------------------------
    # DISPLAY FINAL RICH REPORT
    # ------------------------------------------------------

    display_final_result(result)

    # ------------------------------------------------------
    # GENERATE ONE COMPLETE PDF
    # ------------------------------------------------------

    console.print()

    console.print(
        "[bold cyan]Generating complete travel PDF...[/bold cyan]"
    )

    pdf_path = generate_travel_pdf(result)

    console.print()

    console.print(
        Panel(
            "[bold green]✓ PDF generated successfully![/bold green]\n\n"
            f"[white]File:[/white] {pdf_path}\n\n"
            "[dim]Request + Specialist Findings + Final Itinerary[/dim]",
            title="[bold green]COMPLETE TRAVEL REPORT[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


# ==========================================================
# 15. APPLICATION ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        console.print(
            "\n[bold yellow]Travel planning interrupted.[/bold yellow]"
        )

    except Exception as error:

        console.print()

        console.print(
            Panel(
                f"[bold red]{type(error).__name__}[/bold red]\n\n{error}",
                title="[bold red]APPLICATION ERROR[/bold red]",
                border_style="red",
            )
        )

        raise
