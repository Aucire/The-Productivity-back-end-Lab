
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Note


notes_bp = Blueprint("notes", __name__, url_prefix="/api/notes")

VALID_PRIORITIES = {"Low", "Medium", "High"}


def get_user_note(note_id):
    user_id = int(get_jwt_identity())

    return Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()


@notes_bp.route("", methods=["POST"])
@jwt_required()
def create_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"message": "A valid JSON object is required."}), 400

    title = data.get("title")
    content = data.get("content")
    category = data.get("category", "General")
    priority = data.get("priority", "Medium")
    completed = data.get("completed", False)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"message": "Title is required."}), 400

    if not isinstance(content, str) or not content.strip():
        return jsonify({"message": "Content is required."}), 400

    if not isinstance(category, str) or not category.strip():
        return jsonify({"message": "Category is required."}), 400

    if not isinstance(priority, str) or priority not in VALID_PRIORITIES:
        return jsonify({
            "message": "Priority must be Low, Medium or High."
        }), 400

    if not isinstance(completed, bool):
        return jsonify({
            "message": "Completed must be true or false."
        }), 400

    note = Note(
        title=title.strip(),
        content=content.strip(),
        category=category.strip(),
        priority=priority,
        completed=completed,
        user_id=int(get_jwt_identity())
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        "message": "Note created successfully.",
        "note": note.to_dict()
    }), 201


@notes_bp.route("", methods=["GET"])
@jwt_required()
def get_notes():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        if page < 1 or per_page < 1:
            raise ValueError

        per_page = min(per_page, 100)

    except ValueError:
        return jsonify({
            "message": "Page and per_page must be positive numbers."
        }), 400

    user_id = int(get_jwt_identity())

    query = Note.query.filter_by(
        user_id=user_id
    ).order_by(Note.created_at.desc())

    total = query.count()

    notes = query.offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    pages = (total + per_page - 1) // per_page

    return jsonify({
        "notes": [note.to_dict() for note in notes],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_previous": page > 1 and total > 0
        }
    }), 200


@notes_bp.route("/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):
    note = get_user_note(note_id)

    if not note:
        return jsonify({"message": "Note not found."}), 404

    return jsonify({
        "note": note.to_dict()
    }), 200


@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    note = get_user_note(note_id)

    if not note:
        return jsonify({"message": "Note not found."}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"message": "A valid JSON object is required."}), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify({"message": "Invalid title."}), 400
        note.title = data["title"].strip()

    if "content" in data:
        if not isinstance(data["content"], str) or not data["content"].strip():
            return jsonify({"message": "Invalid content."}), 400
        note.content = data["content"].strip()

    if "category" in data:
        if not isinstance(data["category"], str) or not data["category"].strip():
            return jsonify({"message": "Invalid category."}), 400
        note.category = data["category"].strip()

    if "priority" in data:
        if not isinstance(data["priority"], str) or data["priority"] not in VALID_PRIORITIES:
            return jsonify({"message": "Invalid priority."}), 400
        note.priority = data["priority"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({
                "message": "Completed must be true or false."
            }), 400
        note.completed = data["completed"]

    db.session.commit()

    return jsonify({
        "message": "Note updated successfully.",
        "note": note.to_dict()
    }), 200


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    note = get_user_note(note_id)

    if not note:
        return jsonify({"message": "Note not found."}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully."
    }), 200

