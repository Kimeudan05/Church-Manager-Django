Summary of your clean, scalable model architecture
✔ ACCOUNTS

Profile (role, avatar, phone, group)

OneToOne with User

✔ GROUPS

MinistryGroup

GroupMembership

✔ EVENTS

Global events

Group-specific events

Banners, times, locations

✔ SERMONS

Scripture

PDFs, video links

Thumbnails

✔ ATTENDANCE

Scalable attendance tracking

This structure is production-level and perfect for a church management platform.

#### Creating a tag for our releases
- To create a tag `git tag -a v1.0 <commit hash> `
- Add a message then press `esc` and add `:wq` then enter:
- then   `git push origin v1.0`