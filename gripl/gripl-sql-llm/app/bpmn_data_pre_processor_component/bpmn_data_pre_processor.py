import xml.etree.ElementTree as ET

class BPMNDataPreProcessor:

    def __init__(self,):
        self.activity_types = {
            "task",
            "userTask",
            "serviceTask",
            "manualTask",
            "scriptTask",
            "businessRuleTask",
            "sendTask",
            "receiveTask",
            "callActivity",
            "subProcess"
        }


    def get_only_activity_field_of_bpmn_file(self,
                                             bpmn_content,
                                             ):
        try:
            root = ET.fromstring(bpmn_content)

            activities = []

            for element in root.iter():

                tag_name = element.tag.split("}")[-1]

                if tag_name in self.activity_types:
                    activity = ET.tostring(
                        element,
                        encoding="unicode"
                    )

                    activities.append(activity)
            return activities
        except Exception as e:
            print(e)
            return []


