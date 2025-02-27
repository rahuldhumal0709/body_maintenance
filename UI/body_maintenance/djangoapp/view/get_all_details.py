from djangoapp.utilities.view_file_import import *
class Get_all_details(generics.ListCreateAPIView):
    """Get all details of person or using date"""

    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            response_data = []
            data = request.GET
            if 'person_id' in data:
                person_id = data['person_id']
                person_info = bm_person_info.objects.filter(id=person_id)
                brakfast_info = bm_meal.objects.filter(person_id=person_id).order_by('id')
                sql_query = """SELECT sc.station_id, sc.station_name, COUNT(pr.status) AS fail_count
                                FROM djangoapp_trac_static_config sc
                                INNER JOIN djangoapp_trac_product_history pr ON sc.id = pr.station_id
                                WHERE pr.status = 'fail' AND pr.ts = CURRENT_DATE
                                GROUP BY sc.station_id, sc.station_name order by fail_count desc;"""
                cursor.execute(sql_query,)
                person_details_obj = cursor.fetchall()
                
            if len(response_data)==0:
                logger.info(f"Details of given input not found")
                return HttpResponse(
                json.dumps({"status":"failed",
                            "message": "Details of given input not found",
                            "data":response_data}),
                status=200,
                content_type="application/json",
                )
            
            else:
                logger.info(f"Details of given input retrieved successfully")
                return HttpResponse(
                    json.dumps({"status":"success",
                                "message": "Details of given input retrieved successfully",
                                "total":len(response_data),
                                "data":response_data}),
                    status=200,
                    content_type="application/json",
                )
        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps({"status":"failed",
                            "message": "There is backend issue, please contact administrator"}),
                status=200,
                content_type="application/json",
            )
