alias pm="python docker-entrypoint.py"

pm vj4.job.rp recalc_all
pm vj4.job.rank run_all

# 将所有隐藏题目设置为不隐藏
# use vijos4
# db.document.update({"doc_type":10, "hidden":true},{$set:{"hidden":false}},{multi:true})