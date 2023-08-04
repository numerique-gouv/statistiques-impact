function computePercentageSignedCommits(verificationStatuses: boolean[]) {
    let verifiedCount = 0,
        notVerifiedCount = 0;
    verificationStatuses.forEach((verificationStatus) => {
        if (verificationStatus) {
            verifiedCount++;
        } else {
            notVerifiedCount++;
        }
    });
    if (verifiedCount + notVerifiedCount > 0) {
        return verifiedCount / (verifiedCount + notVerifiedCount);
    }
    return 1;
}

export { computePercentageSignedCommits };
