from messaging.message_bus import MessageBus
from messaging.message_types import Message, MessageType
from orchestrator.state_machine import StateMachine, SystemState, Event
from agents.data_parser_agent import DataParserAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.faq_generator_agent import FAQGeneratorAgent
from agents.product_page_generator_agent import ProductPageGeneratorAgent
from agents.comparison_agent import ComparisonAgent
import uuid
import json
import time

class WorkflowOrchestrator:
    """Orchestrator coordinates autonomous agents via message passing."""

    def __init__(self):
        self.orchestrator_id = "orchestrator"
        self.message_bus = MessageBus()
        self.state_machine = StateMachine()
        self.conversation_id = str(uuid.uuid4())
        self.workflow_data = {}

        # Initialize autonomous agents
        self.agents = self._initialize_agents()

        # Register state actions
        self._register_state_actions()

        # Register orchestrator with message bus
        self.message_bus.register_agent(self.orchestrator_id)

        print(f"[{self.orchestrator_id}] Orchestrator initialized with message-based coordination")

    def _initialize_agents(self):
        """Initialize and start autonomous agents."""
        agents = {
            "parser": DataParserAgent("data_parser", self.message_bus),
            "question_gen": QuestionGeneratorAgent("question_generator", self.message_bus),
            "faq_gen": FAQGeneratorAgent("faq_generator", self.message_bus),
            "product_gen": ProductPageGeneratorAgent("product_page_generator", self.message_bus),
            "comparison_gen": ComparisonAgent("comparison_generator", self.message_bus),
        }

        # Start all agents (they run independently now)
        for agent in agents.values():
            agent.start()

        print(f"[{self.orchestrator_id}] All agents started autonomously\n")
        return agents

    def _register_state_actions(self):
        """Register actions triggered by state transitions."""
        self.state_machine.register_action(
            SystemState.PARSING_DATA,
            self._request_data_parsing
        )
        self.state_machine.register_action(
            SystemState.GENERATING_QUESTIONS,
            self._request_question_generation
        )
        self.state_machine.register_action(
            SystemState.GENERATING_FAQ,
            self._request_faq_generation
        )
        self.state_machine.register_action(
            SystemState.GENERATING_PRODUCT_PAGE,
            self._request_product_page_generation
        )
        self.state_machine.register_action(
            SystemState.GENERATING_COMPARISON,
            self._request_comparison_generation
        )

    def run_pipeline(self, raw_data: dict):
        """Run coordinated multi-agent pipeline."""
        print(f"{'='*70}")
        print(f"[{self.orchestrator_id}] Starting Autonomous Multi-Agent Pipeline")
        print(f"Conversation ID: {self.conversation_id}")
        print(f"{'='*70}\n")

        self.workflow_data["input"] = raw_data

        # Trigger initial state transition
        self.state_machine.trigger(Event.START_PIPELINE)

        # Listen for agent responses and coordinate workflow
        self._coordinate_workflow()

    def _request_data_parsing(self):
        """Request data parsing from autonomous agent."""
        print(f"\n[{self.orchestrator_id}] Requesting data parsing...\n")
        message = Message(
            sender=self.orchestrator_id,
            receiver="data_parser",
            message_type=MessageType.REQUEST,
            content={
                "action": "parse_data",
                "data": self.workflow_data["input"]
            },
            timestamp=None,
            conversation_id=self.conversation_id
        )
        self.message_bus.send_message(message)

    def _request_question_generation(self):
        """Request question generation from autonomous agent."""
        print(f"\n[{self.orchestrator_id}] Requesting question generation...\n")
        message = Message(
            sender=self.orchestrator_id,
            receiver="question_generator",
            message_type=MessageType.REQUEST,
            content={"action": "generate_questions"},
            timestamp=None,
            conversation_id=self.conversation_id
        )
        self.message_bus.send_message(message)

    def _request_faq_generation(self):
        """Request FAQ generation from autonomous agent."""
        print(f"\n[{self.orchestrator_id}] Requesting FAQ page generation...\n")
        message = Message(
            sender=self.orchestrator_id,
            receiver="faq_generator",
            message_type=MessageType.REQUEST,
            content={
                "action": "generate_faq",
                "product": self.workflow_data.get("product"),
                "questions": self.workflow_data.get("questions")
            },
            timestamp=None,
            conversation_id=self.conversation_id
        )
        self.message_bus.send_message(message)

    def _request_product_page_generation(self):
        """Request product page generation from autonomous agent."""
        print(f"\n[{self.orchestrator_id}] Requesting product page generation...\n")
        message = Message(
            sender=self.orchestrator_id,
            receiver="product_page_generator",
            message_type=MessageType.REQUEST,
            content={
                "action": "generate_product_page",
                "product": self.workflow_data.get("product")
            },
            timestamp=None,
            conversation_id=self.conversation_id
        )
        self.message_bus.send_message(message)

    def _request_comparison_generation(self):
        """Request comparison generation from autonomous agent."""
        print(f"\n[{self.orchestrator_id}] Requesting comparison page generation...\n")
        message = Message(
            sender=self.orchestrator_id,
            receiver="comparison_generator",
            message_type=MessageType.REQUEST,
            content={
                "action": "generate_comparison",
                "product": self.workflow_data.get("product")
            },
            timestamp=None,
            conversation_id=self.conversation_id
        )
        self.message_bus.send_message(message)

    def _coordinate_workflow(self):
        """Listen for agent responses and dynamically coordinate workflow."""
        while self.state_machine.current_state != SystemState.COMPLETED:
            message = self.message_bus.receive_message(self.orchestrator_id, timeout=1)

            if message and message.conversation_id == self.conversation_id:
                self._handle_agent_response(message)

            time.sleep(0.1)

        print(f"\n{'='*70}")
        print(f"[{self.orchestrator_id}] Pipeline Completed Successfully!")
        print(f"{'='*70}\n")
        self._shutdown_agents()

    def _handle_agent_response(self, message: Message):
        """Handle responses from autonomous agents and trigger state transitions."""
        if message.message_type == MessageType.RESPONSE:
            content = message.content

            if message.sender == "data_parser":
                print(f"\n[{self.orchestrator_id}] Received parsed product data\n")
                self.workflow_data["product"] = content["product"]
                self.state_machine.trigger(Event.DATA_PARSED)

            elif message.sender == "question_generator":
                print(f"\n[{self.orchestrator_id}] Received {content['count']} generated questions\n")
                self.workflow_data["questions"] = content["questions"]
                self.state_machine.trigger(Event.QUESTIONS_GENERATED)

            elif message.sender == "faq_generator":
                print(f"\n[{self.orchestrator_id}] Received FAQ page\n")
                self.workflow_data["faq_page"] = content["faq_page"]
                self._save_json(content["faq_page"], "output/faq.json")
                self.state_machine.trigger(Event.FAQ_GENERATED)

            elif message.sender == "product_page_generator":
                print(f"\n[{self.orchestrator_id}] Received product page\n")
                self.workflow_data["product_page"] = content["product_page"]
                self._save_json(content["product_page"], "output/product_page.json")
                self.state_machine.trigger(Event.PRODUCT_PAGE_GENERATED)

            elif message.sender == "comparison_generator":
                print(f"\n[{self.orchestrator_id}] Received comparison page\n")
                self.workflow_data["comparison_page"] = content["comparison_page"]
                self._save_json(content["comparison_page"], "output/comparison_page.json")
                self.state_machine.trigger(Event.COMPARISON_GENERATED)

        elif message.message_type == MessageType.ERROR:
            print(f"\n[{self.orchestrator_id}] Error from {message.sender}: {message.content}\n")
            self.state_machine.current_state = SystemState.ERROR

    def _save_json(self, data: dict, filepath: str):
        """Save data as JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved: {filepath}")

    def _shutdown_agents(self):
        """Gracefully shutdown all autonomous agents."""
        print(f"\n[{self.orchestrator_id}] Shutting down agents...\n")
        for agent in self.agents.values():
            agent.stop()
        print(f"[{self.orchestrator_id}] All agents shut down\n")
