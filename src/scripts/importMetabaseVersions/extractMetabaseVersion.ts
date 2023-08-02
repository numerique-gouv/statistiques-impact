const VERSION_REGEX = /v\d+(\.\d+){2,3}/;

async function extractMetabaseVersion(html: string) {
    const search = html.match(VERSION_REGEX);
    if (!search) {
        return undefined;
    }
    const metabaseVersion = search[0];
    return metabaseVersion;
}

export { extractMetabaseVersion, VERSION_REGEX };
