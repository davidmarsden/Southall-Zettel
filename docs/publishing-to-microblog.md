# Publishing from Southall-Zettel to Southall Stories

Southall-Zettel normally mirrors live Southall Stories automatically. Reverse publishing is deliberately manual and opt-in.

## Safety model

Publishing requires **both** of these actions:

1. Add `publish_to_microblog: true` to the YAML front matter of exactly one file under `posts/**` and commit the edit.
2. Manually run the GitHub Actions workflow **Publish Zettel post to Southall Stories**.

Nothing under `posts/**` is automatically published merely because it changes in GitHub.

The first version replaces **only the existing post body** through Micro.blog's Micropub `action=update`. It does not create posts, delete posts, change titles, or change categories.

Before publishing, the script confirms that the target URL belongs to Southall Stories and already exists in Micro.blog's `q=source` results. After Micro.blog accepts the update, it fetches the live post again and compares the returned content with the Zettel body.

Only after that verification succeeds does it remove `publish_to_microblog: true`. The workflow commits that housekeeping change as `Confirm Southall Stories publish`.

If verification fails, the workflow fails and the publish flag remains in the post for investigation/retry.

## Running it

In GitHub:

1. Open **Actions**.
2. Choose **Publish Zettel post to Southall Stories**.
3. Choose **Run workflow**.
4. Optionally enter the exact repository path, for example `posts/2026/05/25/feeling-the-heat.md`.

Even when a path is supplied, the file must still contain `publish_to_microblog: true`.

If no path is supplied, the publisher scans `posts/**` for the flag. For safety it refuses to continue if more than one post is flagged at the same time.

## Normal editorial loop

1. Edit an existing article in Southall-Zettel.
2. Review the Git diff.
3. Add `publish_to_microblog: true` when ready.
4. Commit the change.
5. Run the manual publish workflow.
6. The publisher updates Micro.blog and verifies the live source.
7. The flag is removed and committed automatically.
8. That post commit triggers the normal Southall-Zettel research rebuild, keeping the corpus and derived indexes in sync.
