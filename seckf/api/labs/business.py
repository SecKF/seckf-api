from seckf.api.labs.deletion_tasks import SKFLabDelete
from seckf.api.labs.deployment_tasks import SKFLabDeployment
from seckf.api.security import log
from seckf.database.lab_items import LabItem


def get_labs():
    log("User requested list of kb items", "LOW", "PASS")
    result = LabItem.query.order_by(LabItem.level.asc()).paginate(1, 2500, False)
    return result


def deploy_labs(instance_id, userid):
    log("User requested deployment of lab", "LOW", "PASS")
    result = LabItem.query.filter(LabItem.id == instance_id).first()
    rpc = SKFLabDeployment()
    body = result.image_tag + ":" + str(userid)
    response = rpc.call(body)
    return response


def delete_labs(instance_id, userid):
    log("User requested depletion of lab", "LOW", "PASS")
    result = LabItem.query.filter(LabItem.id == instance_id).first()
    rpc = SKFLabDelete()
    body = result.image_tag + ":" + str(userid)
    response = rpc.call(body)
    return response
