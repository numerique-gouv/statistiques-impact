function parseGithubUrl(githubUrl: string) {
    const GITHUB_URL_REGEX = /https:\/\/github\.com\/(.*)\/(.*)\/?/;
    const result = githubUrl.match(GITHUB_URL_REGEX);
    if (!result || result.length !== 3) {
        throw new Error(
            `githubUrl ${githubUrl} does not match regex : could not extract repository owner and name`,
        );
    }

    return { owner: result[1], name: result[2] };
}

export { parseGithubUrl };
