# Tool Selection Agent

You can always manually call a specific tool by entering a tool name prefixed with `@`.  You can even call multiple tools in a single request.  Read https://github.com/eliranwong/toolmate/blob/main/package/toolmate/docs/Supported%20Backends%20and%20Models.md

To automate the tool selection process, ToolMate AI offers a `Tool Selection Agent` built-in for such purpose. When `Tool Selection Agent` is enabled, it recommends appropriate tools to resolve your requests.

# Automatic Tool Selection

With the `Tool Selection Agent` enabled, you have the additional option to enable `Automatic Tool Selection`. This allows the `Tool Selection Agent` to automatically apply the first recommended tool for each request. The `Tool Selection Agent` may recommend multiple tools to resolve a single request. You can enable the `Automatic Tool Selection` option to automatically use the most relevant tool, or disable the option to manually select a tool from the recommendations. With manual selection, you can choose the `chat only` option, which outputs only LLM-based response without use of any third-party tools, or select `more ...` to view and choose from all enabled tools.

# Configurations

You can enable / disable `Tool Selection Agent` in `Automatic Tool Selection` in one of the following ways:

* Select `configure tool selection agent` from [Action Menu](https://github.com/eliranwong/toolmate/blob/main/package/toolmate/docs/Action%20Menu.md)

* Enter `.tools` in ToolMate AI prompt.
