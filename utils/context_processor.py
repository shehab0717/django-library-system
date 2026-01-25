def active_link(request):
    url: str = request.path
    if url.startswith("/book/author"):
        return {"active_link": "authors"}
    if url.startswith("/book/"):
        return {"active_link": "books"}
    if url.startswith("/member/"):
        return {"active_link": "members"}
    if url.startswith("/circulation/"):
        return {"active_link": "circulations"}

    return {"active_link": "home"}
