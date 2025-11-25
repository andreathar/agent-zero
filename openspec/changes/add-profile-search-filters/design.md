# Design: Profile Search Filters

## Architecture
- **Frontend**: Add filter dropdowns/inputs to the Profile List component.
- **Backend**: Update the profile search API to accept `role` and `team` parameters.
- **Database**: Ensure `role` and `team` fields are indexed for performance if necessary.

## UI/UX
- Two new dropdowns above the profile list: "Role" and "Team".
- Selecting a value triggers a re-fetch of the profile list.
