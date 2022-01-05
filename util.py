def get_domain_from_origin(origin):
    if origin is None:
        return origin

    return origin \
        .replace("https", "") \
        .replace("http", "") \
        .replace("://", "") \
        .replace("www.", "") \
        .replace(":8080", "") \
        .replace(":80", "") \
        .replace(":443", "")
