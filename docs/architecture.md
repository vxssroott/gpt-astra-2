# 🏗️ ASTRA 2.0: Technical Architecture

## Cognitive Flow
ASTRA 2.0 operates as a Finite State Machine (FSM). Each transition is gated by an epistemic check.

### The State Transition Matrix
| From | To | Trigger |
| :--- | :--- | :--- |
| Perception | Hypothesis | Intent extraction complete |
| Hypothesis | Execution | Strategy validated |
| Execution | Verification | Data collection complete |
| Verification | Reflection | Confidence < Threshold |
| Reflection | Hypothesis | Hypothesis mutated |

## Data Model
Memory is stored as a MultiDiGraph $\mathcal{G} = (V, E)$, where $V$ are entities and $E$ are predicates.
