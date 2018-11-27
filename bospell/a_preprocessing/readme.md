# Preprocessing (optional)

Cleaning up the string is done in this pipe. 

## Expected In/Out

 - Input: `string`
 - Output: `string`

## Content

| component signature                                 |  action                                                |
|-----------------------------------------------------|--------------------------------------------------------|
| `def basic_cleanup(text: str) -> str:`               | <ul><li>replaces `\n`s with spaces</li><li>reduces multiple spaces</li></ul> | 
| `def corpus_cleanup(text: str) -> str:`             | <ul><li>remove the literary alternatives to the vernacular words</li><li>strip corpus markup `['༼', '༽', '༜', '༙', '#', '$', '༺', '༻']`</li><li>leave segmentation correction marks `[` and `]`</li><li>reduce multiple spaces</li></ul> |
| `def corpus_cleanup_vernacular(text: str) -> str:`  | <ul><li>remove the literary alternatives to the vernacular words</li><li>strip corpus markup `['༼', '༽', '༜', '༙', '#', '$', ']', '[']`</li><li>leave vernacular marks `༺`, `༻`</li><li>reduce multiple spaces</li></ul> |