# Better execute these commands on terminal
# 1. Enter the current dir path
# 2. Use python and enter >>> input mode
from myTable import db
from myTable import BlogPost

# Neccessary: Use this to build the .db, the main table and the columns only for the first time.
# db.create_all()

    # SQL INSERT db.session.add
# data = BlogPost(title='three', content='Fuck!!!', author='Leo')
# db.session.add(data)
# db.session.commit()

#   # SQL SELECT BlogPost.query
# data = BlogPost.query.all() 
# # ORDER BY
# data = BlogPost.query.order_by.all()
# # Single data user  .query.all()[3] or .query.get(3) or .query[3] are the same
# data = BlogPost.query[2]
# # Get a specific column (it has to be only one data selected)
# data = BlogPost.query[2].title
# # WHERE ****This method still return a thing contain several datas even it seems only one data
# data = BlogPost.query.filter_by(id=1).all() 
# get_or_404 will raise 404 exception if nothing match the condition
data = BlogPost.query.first()
print(data)
   # SQL DELETE db.session.delete(SELECT syntax)
# db.session.delete(BlogPost.query.....)
# db.session.commit() 

#   # SQL UPDATE  
# BlogPost.query[3].author = 'Nina'
# db.session.commit()