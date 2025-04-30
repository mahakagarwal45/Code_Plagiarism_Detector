def fresh(self) -> bool:
        """
        检查请求缓存是否“新鲜”，也就是内容没有改变。
        此方法用于 If-None-Match / ETag, 和 If-Modified-Since 和 Last-Modified 之间的缓存协商。
        在设置一个或多个这些响应头后应该引用它。
        """
        method_str = self.method
        if method_str != 'GET' and method_str != 'HEAD':
            return False
        s = self.ctx.status
        if (s >= 200 and s < 300) or s == 304:
            return fresh(
                self.headers,
                (self.response and self.response.headers) or {},
            )
        return False