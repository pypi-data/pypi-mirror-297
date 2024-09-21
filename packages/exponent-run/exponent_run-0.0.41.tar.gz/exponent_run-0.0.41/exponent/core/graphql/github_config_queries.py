CREATE_GITHUB_CONFIG_MUTATION: str = """
    mutation CreateGithubConfig(
        $githubPat: String!,
    ) {
        createGithubConfig(
            githubPat: $githubPat
        ) {
            __typename
            ... on GithubConfig {
                githubConfigUuid
                githubPat
            }
        }
    }
"""
