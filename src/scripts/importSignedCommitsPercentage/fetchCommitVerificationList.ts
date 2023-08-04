import axios from 'axios';
import { computeBeginningDateToWatch } from './computeBeginningDateToWatch';
import { parseGithubUrl } from './parseGithubUrl';

const GITHUB_API_VERSION = '2022-11-28';

const MONTHS_TO_WATCH = 2;

type githubCommitApiType = Array<{
    commit: {
        verification: { verified: boolean };
    };
}>;

async function fetchCommitVerificationList(repositoriesUrl: string[]) {
    const verificationStatuses: boolean[] = [];
    for (const repositoryUrl of repositoriesUrl) {
        const repository = parseGithubUrl(repositoryUrl);
        let page = 1;
        let hasReachedLastPage = false;
        do {
            const githubApiUrl = computeGithubCommitsApiUrl(repository, {
                since: computeBeginningDateToWatch(new Date(), MONTHS_TO_WATCH),
                page,
            });
            const result = await axios.get<githubCommitApiType>(githubApiUrl, {
                headers: { 'X-GitHub-Api-Version': GITHUB_API_VERSION },
            });
            result.data.forEach(({ commit }) => {
                verificationStatuses.push(commit.verification.verified);
            });
            hasReachedLastPage = result.data.length !== 0;
            page++;
        } while (hasReachedLastPage);
    }
    return verificationStatuses;
}

function computeGithubCommitsApiUrl(
    repository: { owner: string; name: string },
    query: { since: string; page: number },
) {
    return `https://api.github.com/repos/${repository.owner}/${repository.name}/commits?since=${query.since}&per_page=100&page=${query.page}`;
}

export { fetchCommitVerificationList };
