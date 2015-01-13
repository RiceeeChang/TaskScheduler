class Project(object):
    def __init__(self, project):
        self.projectID    = project['projectID']
        self.userID       = project['userID']
        self.appID        = project['appID']
        self.appType      = project['appType']
        self.budget       = project['budget']
        self.creationDate = project['creationDate']

        self.priority = countPriority(self.userID, self.budget)
        self.app      = getApp(self.appID)

        self.task_list = []

