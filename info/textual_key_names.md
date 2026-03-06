# Textual Key Name Attributes for Non-Alphanumeric Characters

In Textual, the `name` attribute for printable special characters follows Unicode character name conventions (lowercased, spaces replaced with `_`).

| Character | `name` |
|---|---|
| `` ` `` | `grave_accent` |
| `~` | `tilde` |
| `!` | `exclamation_mark` |
| `@` | `commercial_at` |
| `#` | `number_sign` |
| `$` | `dollar_sign` |
| `%` | `percent_sign` |
| `^` | `circumflex_accent` |
| `&` | `ampersand` |
| `*` | `asterisk` |
| `(` | `left_parenthesis` |
| `)` | `right_parenthesis` |
| `-` | `minus` |
| `_` | `underscore` |
| `=` | `equals_sign` |
| `+` | `plus_sign` |
| `[` | `left_square_bracket` |
| `]` | `right_square_bracket` |
| `{` | `left_curly_bracket` |
| `}` | `right_curly_bracket` |
| `\` | `reverse_solidus` |
| `\|` | `vertical_line` |
| `;` | `semicolon` |
| `:` | `colon` |
| `'` | `apostrophe` |
| `"` | `quotation_mark` |
| `,` | `comma` |
| `.` | `full_stop` |
| `<` | `less_than_sign` |
| `>` | `greater_than_sign` |
| `/` | `solidus` |
| `?` | `question_mark` |

## Notes

- Use `on_key` to empirically verify: `self.log(f"key={event.key!r}  name={event.name!r}")`
- Run with `textual run --dev yourapp.py` to see the dev console
- Per-key handler methods are named `key_<name>`, e.g. `key_exclamation_mark`
