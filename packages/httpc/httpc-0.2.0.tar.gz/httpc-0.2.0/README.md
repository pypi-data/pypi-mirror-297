# httpc

**httpx with CSS**

## Examples

```python
>>> import httpc
>>> response = httpc.get("https://www.python.org/")
>>> response.css("strong")  # CSS Query
[<Node strong>, <Node strong>, <Node strong>]
>>> response.css("strong").bc.text()
['Notice:', 'A A', 'relaunched community-run job board']
>>> response.single("div")
ValueError: Query 'div' matched with 47 nodes.
>>> response.single("#content")
<Node div>
>>> httpc.get("https://python.org")                 
<Response [301 Moved Permanently]>
>>> httpc.common.get("https://python.org") 
<Response [200 OK]>
>>> httpc.get("https://httpbin.org/status/400")
<Response [400 BAD REQUEST]>
>>> httpc.get("https://httpbin.org/status/400", raise_for_status=True)
httpx.HTTPStatusError: Client error '400 BAD REQUEST' for url 'https://httpbin.org/status/400'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
```
