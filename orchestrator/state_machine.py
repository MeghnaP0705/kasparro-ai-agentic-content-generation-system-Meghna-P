from enum import Enum
from typing import Dict, Callable

class SystemState(Enum):
    """System states for workflow."""
    IDLE = "idle"
    PARSING_DATA = "parsing_data"
    GENERATING_QUESTIONS = "generating_questions"
    GENERATING_FAQ = "generating_faq"
    GENERATING_PRODUCT_PAGE = "generating_product_page"
    GENERATING_COMPARISON = "generating_comparison"
    COMPLETED = "completed"
    ERROR = "error"

class Event(Enum):
    """Events that trigger state transitions."""
    START_PIPELINE = "start_pipeline"
    DATA_PARSED = "data_parsed"
    QUESTIONS_GENERATED = "questions_generated"
    FAQ_GENERATED = "faq_generated"
    PRODUCT_PAGE_GENERATED = "product_page_generated"
    COMPARISON_GENERATED = "comparison_generated"
    ERROR_OCCURRED = "error_occurred"

class StateMachine:
    """Finite state machine for workflow coordination."""

    def __init__(self):
        self.current_state = SystemState.IDLE
        self.transitions: Dict[tuple, SystemState] = self._define_transitions()
        self.state_actions: Dict[SystemState, Callable] = {}

    def _define_transitions(self) -> Dict[tuple, SystemState]:
        """Define valid state transitions."""
        return {
            (SystemState.IDLE, Event.START_PIPELINE): SystemState.PARSING_DATA,
            (SystemState.PARSING_DATA, Event.DATA_PARSED): SystemState.GENERATING_QUESTIONS,
            (SystemState.GENERATING_QUESTIONS, Event.QUESTIONS_GENERATED): SystemState.GENERATING_FAQ,
            (SystemState.GENERATING_FAQ, Event.FAQ_GENERATED): SystemState.GENERATING_PRODUCT_PAGE,
            (SystemState.GENERATING_PRODUCT_PAGE, Event.PRODUCT_PAGE_GENERATED): SystemState.GENERATING_COMPARISON,
            (SystemState.GENERATING_COMPARISON, Event.COMPARISON_GENERATED): SystemState.COMPLETED,
        }

    def trigger(self, event: Event) -> bool:
        """Trigger state transition."""
        transition = (self.current_state, event)

        if transition in self.transitions:
            new_state = self.transitions[transition]
            print(f"[StateMachine] State transition: {self.current_state.value} -> {new_state.value}")
            self.current_state = new_state

            # Execute state action if defined
            if new_state in self.state_actions:
                self.state_actions[new_state]()

            return True
        else:
            print(f"[StateMachine] Invalid transition: {self.current_state.value} -x-> {event.value}")
            return False

    def register_action(self, state: SystemState, action: Callable):
        """Register action to execute when entering a state."""
        self.state_actions[state] = action
