from prp.controllers import (
    alert_bp, party_state_bp, rating_bp, status_bp
)

def init_routes(app):
    # Childs
    party_state_bp.register_blueprint(alert_bp)
    party_state_bp.register_blueprint(rating_bp)
    party_state_bp.register_blueprint(status_bp)
    
    app.register_blueprint(party_state_bp)