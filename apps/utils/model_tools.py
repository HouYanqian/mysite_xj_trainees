import datetime

from attendance.models import AttendanceRecord
from rbac.models import Menu


def attendance_record_cur_status(user, is_enter=False):
    """
    如果没有当天打卡记录则从排版中新增空白记录，如果有返回状态
    :param user: user object
    :param is_enter: 是否直接录入对应时间
    :return: [当天考勤记录], 上班打卡|下班打卡
    """
    status = ''
    while True:
        attendance_record = user.attendancerecord_set.all().filter(
            shift_start_time__date=datetime.date.today()).order_by('shift_start_time')
        if attendance_record:
            cur_time = datetime.datetime.now()
            # 如果超过最晚班次的下班时间为下班打卡
            if cur_time >= attendance_record.last().shift_end_time:
                status = '下班打卡'
                if is_enter:
                    cur_record = attendance_record.last()
                    cur_record.end_time = cur_time
                    cur_record.save()
            # 如果超过最晚班次上班时间
            elif cur_time >= attendance_record.last().shift_start_time:
                # 如果打过卡为下班时间
                if attendance_record.last().start_time:
                    status = '下班打卡'
                    if is_enter:
                        cur_record = attendance_record.last()
                        cur_record.end_time = cur_time
                        cur_record.save()
                # 如果没打过卡为上班时间
                else:
                    status = '上班打卡'
                    if is_enter:
                        cur_record = attendance_record.last()
                        cur_record.start_time = cur_time
                        cur_record.save()
            # 如果超过最早班次下班时间
            elif cur_time >= attendance_record.first().shift_end_time:
                # 如果打过卡为上班时间
                if attendance_record.first().end_time:
                    status = '上班打卡'
                    if is_enter:
                        cur_record = attendance_record.last()
                        cur_record.start_time = cur_time
                        cur_record.save()
                # 如果没打过卡为下班时间
                else:
                    status = '下班打卡'
                    if is_enter:
                        cur_record = attendance_record.first()
                        cur_record.end_time = cur_time
                        cur_record.save()
            # 如果超过最早班次上班班时间
            elif cur_time >= attendance_record.first().shift_start_time:
                # 如果打过卡为下班时间
                if attendance_record.first().end_time:
                    status = '下班打卡'
                    if is_enter:
                        cur_record = attendance_record.first()
                        cur_record.end_time = cur_time
                        cur_record.save()
                # 如果没打过卡为上班时间
                else:
                    status = '上班打卡'
                    if is_enter:
                        cur_record = attendance_record.first()
                        cur_record.start_time = cur_time
                        cur_record.save()
            # 如果没超过最早班次上班时间为上班打卡
            else:
                status = '上班打卡'
                if is_enter:
                    cur_record = attendance_record.first()
                    cur_record.start_time = cur_time
                    cur_record.save()

            return attendance_record, status
        else:
            # 获取考勤组中的排班新建考勤记录
            attendance_group = user.attendancegroup_set.all().first()
            if attendance_group:
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                for shift in attendance_group.shift.split(', '):
                    start_time, end_time = shift.split(' - ')
                    new_attendance_record = AttendanceRecord(
                        shift_start_time=today + ' ' + start_time,
                        shift_end_time=today + ' ' + end_time,
                        personnel=user
                    )
                    new_attendance_record.save()
            else:
                break
    return attendance_record, status


def get_role_permissions_trees():
    """
    获取角色权限树
    :param role:
    :return:
    """
    role_permission_list = []
    for menu in Menu.objects.filter(parent=None):
        role_permission_list.append({
            'title': menu.title,
            'id': menu.id,
            'children': get_children_trees(menu),
            'spread': 'true',
        })
    return role_permission_list


def get_children_trees(item):
    """
    获取家族树
    :param item: role queryset
    :return:
    """
    children_list = []
    children = item.menu_set.all()
    for child in children:
        children_list.append({
            'title': child.title,
            'id': child.id,
            # 'field': '',
            'children': get_children_trees(child),
            # 'href': '',
            'spread': '',
        })
    return children_list
