# User
- individual user, which is used for login,verification,authentication
- part of 0-n organizations with org roles
- part of 0-n teams with team roles
- part of 0-n projects 
    - via teams with team role or individual role
    - individually with individual role
    
# Organisation
- creates projects, let's teams and/or users join projects

## Member Roles
- Viewer
    - can view organization details, read-only
- Maintainer
    - all viewers privileges
    - can change organization details
    - can create/delete projects
- Owner
    - all maintainers privileges
    - can change organization details
    - can invite / add members
    - can change roles of existing members
    - can remove members

# Team
- group of users working on 0-n projects
- always publicly visible

## Member Roles
- Regular
    - can contribute to the projects of the team
- Admin
    - all regular things
    - can change team info's
    - can invite / add new members
    - can remove members

#Project
- owned by an organization
- has members
    - via 0-n teams
    - via 0-n individuals

## Member Roles
- Viewer
- 
- Creator (all organizations Maintainers + Admins) 
	
# Login

User 1:1 Login

Organisation m:n User (an organization can have many users, a user can be part of many organizations)
An organisation can have multiple teams