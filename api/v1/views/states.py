#!/usr/bin/python3
""" State objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State  # Import the State model

# Retrieves the list of all State objects
@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """gsdf"""
    states = State.get_all_states()  # Implement this method in your State model
    return jsonify([state.to_dict() for state in states])

# Retrieves a State object
@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """gsdf"""
    state = State.get_state_by_id(state_id)  # Implement this method in your State model
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

# Deletes a State object
@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """gsdf"""
    state = State.get_state_by_id(state_id)  # Implement this method in your State model
    if state is None:
        abort(404)
    state.delete()  # Implement this method in your State model
    return jsonify({})

# Creates a State
@app.route('/api/v1/states', methods=['POST'])
def create_state():
    """gsdf"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_state = State(name=data['name'])  # Assuming 'name' is required for State creation
    new_state.save()  # Implement this method in your State model to save the new State
    return jsonify(new_state.to_dict()), 201

# Updates a State object
@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """gsdf"""
    state = State.get_state_by_id(state_id)  # Implement this method in your State model
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    # Update the state attributes except for 'id', 'created_at', 'updated_at'
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()  # Implement this method in your State model to update the State
    return jsonify(state.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
