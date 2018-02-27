Annotation
====================
@RequestMapping("/path") over a method to map HTTP requests.

@RequestMapping maps all HTTP method (GET, PUT, POST, ...) by default, use `@RequestMapping(method = RequestMethod.GET)` to specify a HTTP method for mapping.

@RequestParam(value="name", defaultValue="default") to bind a HTTP argument named "name" with default value "default" if no such HTTP argument received.
