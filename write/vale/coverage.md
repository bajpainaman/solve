# STE rule coverage

Generated from the condensed Issue 9 rule map. Partial checks do not establish compliance.

`STE100Dictionary` rules come from the upstream full-book dictionary build.
This fork excludes that build. Review those rows in context here.

| Rule | Status | Vale checks | Remaining review |
| --- | --- | --- | --- |
| 1.1 | partial | `STE100.WordReview_acceptable`, `STE100.WordReview_alternate`, `STE100.WordReview_avoid`, `STE100.WordReview_both`, `STE100.WordReview_ensure`, `STE100.WordReview_fit`, `STE100.WordReview_follow`, `STE100.WordReview_further`, `STE100.WordReview_however`, `STE100.WordReview_insert`, `STE100.WordReview_main`, `STE100.WordReview_may`, `STE100.WordReview_now`, `STE100.WordReview_perform`, `STE100.WordReview_portion`, `STE100.WordReview_press`, `STE100.WordReview_repeat`, `STE100.WordReview_shall`, `STE100.WordReview_should`, `STE100.WordReview_since`, `STE100.WordReview_therefore`, `STE100.WordReview_using`, `STE100Dictionary.DictionaryWords`, `STE100Dictionary.DictionaryVocabulary` | Uses the skill's curated review map. Alternatives depend on meaning. This is not the full dictionary. The importer retains all extracted non-approved entries. Ambiguous POS, contextual constructions, meanings, and technical-term status require review. Checks approved headwords and listed verb/adjective forms, with approximate noun plurals. This lexical check cannot determine POS, meaning, irregular noun forms, or whether an unknown technical term is valid. |
| 1.2 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.3 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.4 | partial | `STE100Dictionary.DictionaryVocabulary` | Checks approved headwords and listed verb/adjective forms, with approximate noun plurals. This lexical check cannot determine POS, meaning, irregular noun forms, or whether an unknown technical term is valid. |
| 1.5 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.6 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.7 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.8 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.9 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.10 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.11 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.12 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.13 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 1.14 | partial | `STE100.AmericanSpelling` | Curated spelling pairs. Directives, official names, and other spelling differences need review. |
| 2.1 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 2.2 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 3.1 | partial | `STE100Dictionary.DictionaryVocabulary` | Checks approved headwords and listed verb/adjective forms, with approximate noun plurals. This lexical check cannot determine POS, meaning, irregular noun forms, or whether an unknown technical term is valid. |
| 3.2 | partial | `STE100.ComplexTense` | Patterns detect some perfect/progressive constructions. Approved adjective and technical-noun uses need review. |
| 3.3 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 3.4 | partial | `STE100.ComplexTense` | Patterns detect some perfect/progressive constructions. Approved adjective and technical-noun uses need review. |
| 3.5 | partial | `STE100.ComplexTense` | Patterns detect some perfect/progressive constructions. Approved adjective and technical-noun uses need review. |
| 3.6 | partial | `STE100.PassiveVoice` | A past participle can be an adjective. The rule cannot identify the actor or decide whether it is unknown. |
| 3.7 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 4.1 | partial | `STE100Procedure.ProcedureLength`, `STE100Description.DescriptionLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. |
| 4.2 | partial | `STE100.Contractions` | Detects the listed contractions. Omission of necessary words requires review. |
| 4.3 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 4.4 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 4.5 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 5.1 | partial | `STE100Procedure.ProcedureLength`, `STE100Procedure.NoteLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. The full book permits 25 words in NOTE sentences. Recognizes NOTE: paragraphs. Other note markup and sentence boundaries need review. |
| 5.2 | partial | `STE100Procedure.MultipleInstructions` | Matches some pairs of known action verbs. Simultaneous actions and other verbs need review. |
| 5.3 | partial | `STE100Procedure.Imperative` | Flags some indirect instruction openings. Deciding whether a sentence is an instruction needs review. |
| 5.4 | partial | `STE100Procedure.ConditionFirst` | Finds some trailing conditions. Condition scope and comma placement need review. |
| 5.5 | partial | `STE100Procedure.NoteInstructions` | Detects some commands after NOTE:. Other note formats and unlisted verbs need review. |
| 6.1 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 6.2 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 6.3 | partial | `STE100Description.DescriptionLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. |
| 6.4 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 6.5 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 6.6 | partial | `STE100Description.ParagraphSentences` | Sentence boundaries are approximate. Punctuation in abbreviations and quotations can need review. |
| 7.1 | partial | `STE100Safety.RiskLevel` | Finds some CAUTION labels associated with human harm. Symbols, missing labels, and other hazards need review. |
| 7.2 | partial | `STE100Safety.CommandFirst` | Reviews some descriptive openings. Determining the necessary command or condition requires context. |
| 7.3 | partial | `STE100Safety.Consequence` | Absence of a risk keyword is a review prompt. Keywords cannot establish whether the explanation describes the risk correctly. |
| 8.1 | partial | `STE100.Semicolons` | Enforces the semicolon prohibition. Other punctuation still needs review. |
| 8.2 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 8.3 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 8.4 | partial | `STE100Procedure.ProcedureLength`, `STE100Description.DescriptionLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. |
| 8.5 | partial | `STE100Procedure.ProcedureLength`, `STE100Description.DescriptionLength`, `STE100Procedure.NoteLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. The full book permits 25 words in NOTE sentences. Recognizes NOTE: paragraphs. Other note markup and sentence boundaries need review. |
| 8.6 | partial | `STE100Procedure.ProcedureLength`, `STE100Description.DescriptionLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. |
| 8.7 | partial | `STE100Procedure.ProcedureLength`, `STE100Description.DescriptionLength` | Counts parentheses, double quotations, common units, hyphens, and configured proper names. Other names, labels, unusual units, and abbreviations need review. |
| 9.1 | partial | `STE100.WordReview_acceptable`, `STE100.WordReview_alternate`, `STE100.WordReview_avoid`, `STE100.WordReview_both`, `STE100.WordReview_ensure`, `STE100.WordReview_fit`, `STE100.WordReview_follow`, `STE100.WordReview_further`, `STE100.WordReview_however`, `STE100.WordReview_insert`, `STE100.WordReview_main`, `STE100.WordReview_may`, `STE100.WordReview_now`, `STE100.WordReview_perform`, `STE100.WordReview_portion`, `STE100.WordReview_press`, `STE100.WordReview_repeat`, `STE100.WordReview_shall`, `STE100.WordReview_should`, `STE100.WordReview_since`, `STE100.WordReview_therefore`, `STE100.WordReview_using`, `STE100Dictionary.DictionaryWords` | Uses the skill's curated review map. Alternatives depend on meaning. This is not the full dictionary. The importer retains all extracted non-approved entries. Ambiguous POS, contextual constructions, meanings, and technical-term status require review. |
| 9.2 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
| 9.3 | partial | `STE100.PhrasalVerbs` | Uses the existing skill's curated phrase list. Part of speech and unlisted phrases need review. |
| 9.4 | review | None | Requires review of meaning, grammar, terminology, or document structure. |
