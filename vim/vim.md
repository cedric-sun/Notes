Vim Memo
=================

Miscellaneous
-----------------
1. :reg		Display all non-empty registers.
2. C-V C-?	Insert control character.

Scrolling
-----------------
### Scroll by window page
/* N = 1 will be used if N is omitted. */

1. N C-F	Scroll window N pages Forward ( downwards, F for mnemonic).
2. N S-Down	Ditto.
3. N C-B	Scroll window N pages Backward.
4. N S-Up	Ditto.

### Scroll by half window
/* `scroll` by default is the number of lines half of the current window, and will change automatically on the change of the window. Local to window.*/
/* Half window downward scrolling operations here can't move window view downward when there is no content, use */

1. C-D		Scroll downward `scroll` lines.
2. N C-D	Set `scroll` to N first, then C-D.
3. C-U		Scroll upward `scroll` lines.
4. N C-U	Set `scroll` to N first, then C-U.

### Scroll by line(s)
/* N = 1 will be used if N is omitted. */
/

1. N C-E	Scroll downward N lines.
2. N C-Y	Scroll upward N lines
