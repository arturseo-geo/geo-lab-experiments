## E040 Freeze History

**Freeze 1 (1 Oct 2026):** sha256 84dbc9a08e1bae87424de0839b93dfce67f5aadc16e1f5e830a585c223419ff2, commit 7190dbe. Intent column populated by the thegeolab.net/tools/ai-query-intent-classifier/ web tool (5-class). GS-1-A misclassified as COMPARISON due to substring 'or' inside 'framework'. No measurements taken, no DOI assigned.

**Superseded by Freeze 2 (1 Oct 2026):** sha256 e9415f33ab28e676e4613bf689330a0c3c84d9d9610865042f81eeffe61a8571. Reason: the 5-class tool cannot express the design's 4-class taxonomy (DEFINITION, INSTRUCTION, REASON, COMPARISON) and produced a false positive on GS-1-A. The corrected file carries two columns: intent_class_author (the design's taxonomy, author-assigned) and intent_5class_tool (the raw tool output, preserved for transparency). No measurements taken, no DOI assigned at either freeze.
