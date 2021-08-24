module.exports = {
  branches: 'main',
  tagFormat: 'v${version}', // eslint-disable-line no-template-curly-in-string
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    [
      '@google/semantic-release-replace-plugin',
      {
        replacements: [
          {
            files: ['balena.yml'],
            from: 'version: .*',
            to: 'version: ${nextRelease.version}', // eslint-disable-line no-template-curly-in-string
            results: [
              {
                file: 'balena.yml',
                hasChanged: true,
                numMatches: 1,
                numReplacements: 1
              }
            ],
            countMatches: true
          }
        ]
      }
    ],
    ['@semantic-release/git', { assets: ['CHANGELOG.md', 'balena.yml'] }],
    [
      '@semantic-release/github',
      {
        assets: [
          {
            name: 'Scitizen OS (Raspberry Pi 4)',
            path: 'scitizen-os-raspberrypi4-64.img.zip'
          },
          {
            name: 'Scitizen OS (Raspberry Pi 3)',
            path: 'scitizen-os-raspberrypi3-64.img.zip'
          }
        ]
      }
    ]
  ]
}
