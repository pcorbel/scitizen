module.exports = {
  branches: "main",
  tagFormat: "v${version}",
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    [
      "@google/semantic-release-replace-plugin",
      {
        replacements: [
          {
            files: ["balena.yml"],
            from: "version: .*",
            to: "version: v${nextRelease.version}",
            results: [
              {
                file: "balena.yml",
                hasChanged: true,
                numMatches: 1,
                numReplacements: 1,
              },
            ],
            countMatches: true,
          },
        ],
      },
    ],
    ["@semantic-release/git", { assets: ["CHANGELOG.md", "balena.yml"] }],
    "@semantic-release/github",
  ],
};
