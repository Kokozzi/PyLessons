from flask import Flask, request, abort, Response, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import app_config as config
from math import ceil

# Create Flask Application
app = Flask(__name__)
app.config.from_object(config)
# Create database object
db = SQLAlchemy(app)

# Page for retreiving, creating and deleting posts
@app.route("/items", methods=["GET", "POST", "PUT"])
def items():
    from models import GuestBookItem
    from forms import GuestBookForm
    # Retrieve all posts from DB
    if request.method == "GET":
        # Forming querystring for GuestBookItem Model
        qs = GuestBookItem.query
        # Prepare Flask response
        response = Response()
        # Count total number of posts
        total_count = qs.count()
        # Get list of GuestBookItem Columns' names
        keys_names = [column.key for column in GuestBookItem.__table__.columns]
        # List of displaying Columns (empty list means no limitaions)
        fields = []

        # Get filter params from request query
        for key in keys_names:
            if request.args.get(key):
                value = request.args.get(key)
                # Try to detect sign at filter value, then accept filter by required Column
                if value.startswith("<="):
                    qs = qs.filter(GuestBookItem.__table__.columns[key] <= value[2:])
                elif value.startswith(">="):
                    qs = qs.filter(GuestBookItem.__table__.columns[key] >= value[2:])
                elif value.startswith("<"):
                    qs = qs.filter(GuestBookItem.__table__.columns[key] < value[1:])
                elif value.startswith(">"):
                    qs = qs.filter(GuestBookItem.__table__.columns[key] > value[1:])
                else:
                    qs = qs.filter(GuestBookItem.__table__.columns[key] == value)
                # Update querystring posts count
                total_count = qs.count()

        # Get list of fields to display
        if request.args.get("fields"):
            fields = request.args.get("fields").split(",")

        # Response pagination 
        if request.args.get("page") and request.args.get("per_page"):
            per_page = int(request.args.get("per_page"))
            # Calculate total number of pages for this 'per_page' value
            page_limit = ceil(qs.count() / per_page)
            page = int(request.args.get("page"))
            # Trying to acces page outter limit - raise 404
            if page >= page_limit:
                abort(404)
            # Forming urls for first, last, prev and next page (required for 'Link' header)
            first_page = url_for('items', page=0, per_page=per_page, _external=True) + '; rel="first"'
            last_page = url_for('items', page=page_limit-1, per_page=per_page, _external=True) + '; rel="last"'
            if page > 0:
                prev_page = url_for('items', page=max(0,page - 1), per_page=per_page, _external=True) + '; rel="prev"'
            else:
                prev_page = ""
            if page < page_limit - 1:
                next_page = url_for('items', page=min(page_limit - 1, page + 1), per_page=per_page, _external=True) + '; rel="next"'
            else:
                next_page = ""
            # Concat 'Link' header
            link_header = next_page + ", " + last_page + ", " + first_page + ", " + prev_page
            # Append header to response
            response.headers["Link"] = link_header
            # Calculate offset and set queryset limit
            offset = page * per_page
            qs = qs.offset(offset).limit(per_page)

        # Sort result by one of Columns
        if request.args.get("sort"):
            # Get sorting param from request query
            sorting_param = request.args.get("sort")
            # Check sorting order - asc or desc (in case of '-' at the beginnig of param)
            if sorting_param.startswith("-"):
                sorting_param = sorting_param[1:]
                desc = True
            else:
                desc = False
            # Check if sorting param really exist at GuestBookItem model
            if sorting_param in [column.key for column in GuestBookItem.__table__.columns]:
                # Get sorting Column from model
                sorting_column = GuestBookItem.__table__.columns[sorting_param]
                # Apply sorting
                if desc:
                    qs = qs.order_by(sorting_column.desc())
                else:
                    qs = qs.order_by(sorting_column)
        # Empty db
        if total_count == 0:
            response.set_data("Guestbook is empty")
        else:
            posts_list = []
            # Forming list of posts 
            for post in qs:
                # Each post is presented as dict
                posts_list.append(post.as_dict(fields))
            # Return result as JSON
            response.set_data(json.dumps(posts_list))
        # Setting custom header with total count of posts
        response.headers["X-Total-Count"] = total_count
        return response
    # Creating new post
    elif request.method == "POST":
        print(request.form)
        # Receive FORM data from request and appent it to WTForm
        form = GuestBookForm(request.form)
        print(form.data)
        # Validate request data
        if form.validate():
            # Crate new model object
            guest_post = GuestBookItem(**form.data)
            # Save new post to DB
            db.session.add(guest_post)
            print(form.data)
            db.session.commit()
            # Forming 201 code response with JSON body and custom 'Location' header
            response = Response(json.dumps(guest_post.as_dict()))
            response.headers["Location"] = "/items/{}".format(guest_post.id)
            return response, 201
        # Form data failed validation
        else:
            return "Invalid form"
    # Remove all posts from DB
    elif request.method == "PUT":
        # Detect empty request
        if len(request.form) == 0:
            # Remove all posts
            db.session.query(GuestBookItem).delete()
            db.session.commit()
            # Return JSON with empty posts list
            return (json.dumps(GuestBookItem.query.all()))
        return "Error", 400
    else:
        return "Error", 400

# Page for working with separate post (based on 'item_id' value from url)
@app.route("/items/<item_id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def item_detail(item_id):
    from models import GuestBookItem
    # Retrieve info about separate post
    if request.method == "GET":
        # Filter stored posts by ID
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        # Nothing was found, return 404
        if guest_post is None:
            abort(404)
        # Return JSON with post info
        return json.dumps(guest_post.as_dict())
    # Update post info (not all fields)
    elif request.method == "PATCH":
        # Retrieve post id from request
        post_id = request.form.get("id")
        # Post id was not found, return 404
        if post_id is None:
            abort(404)
        # Forming dict with possible info updates - author and text
        update_dict = {}
        author = request.form.get("author")
        if author is not None:
            update_dict["author"] = author
        text = request.form.get("text")
        if text is not None and len(text) >= 5:
            update_dict["text"] = text
        # Nothing to update - return error with 400 code
        if len(update_dict) == 0:
            return "Empty update", 400
        # Find proper post from db
        db_update = db.session.query(GuestBookItem).filter_by(id=post_id)
        if db_update.first() is None:
            abort(404)
        else:
            # Update post info
            db_update.update(update_dict)
        db.session.commit()
        # Retrieve updated info from DB and return as JSON
        guest_post = GuestBookItem.query.filter_by(id=post_id).first()
        return json.dumps(guest_post.as_dict_updated())
    # Update post info (all field required)
    elif request.method == "PUT":
        from forms import GuestBookForm
        post_id = request.form.get("id")
        if post_id is None:
            abort(404)
        # Retrieve form data from request and validate it
        form = GuestBookForm(request.form)
        if form.validate():
            # Update post from DB with new data
            db_update = db.session.query(GuestBookItem).filter_by(id=post_id)
            if db_update.first() is None:
                abort(404)
            else:
                db_update.update(form.data)
            db.session.commit()
            guest_post = GuestBookItem.query.filter_by(id=post_id).first()
            return json.dumps(guest_post.as_dict_updated())
        else:
            return "Invalid form", 400
    # Delete post (set 'is_visible' to 'False')
    elif request.method == "DELETE":
        guest_post = GuestBookItem.query.filter_by(id=item_id).first()
        # Return custom error response with 204 code
        if guest_post is None:
            return "Unknown number", 204
        else:
            # Update post item at DB with new 'is_visible' flag
            db.session.query(GuestBookItem).filter_by(id=item_id).update({"is_visible": False})
            db.session.commit()
            return "Deleted", 200
    else:
        return "Error", 400


if __name__ == "__main__":
    from models import *
    db.create_all()
    app.run()