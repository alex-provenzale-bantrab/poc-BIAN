from .utils._execute_query import _execute_query

class PartyStateRepository:
        
    def selectPartyStateByCustomerReference(self, body):
        query = 'SELECT * FROM PartyState WHERE CustomerReference = ?'
        party_state = _execute_query(query, (body.get('CustomerReference'),)).fetchone()
        return party_state
    
    def selectPartyStateById(self, party_state_id):
        query = 'SELECT * FROM PartyState WHERE PartyStateId = ?'
        party_state = _execute_query(query, (party_state_id,)).fetchone()
        return party_state
    
    def insertPartyState(self, body):
        query = 'INSERT INTO PartyState (CustomerReference) VALUES (?)'
        cursor = _execute_query(query, (body.get('CustomerReference'),), commit=True)
        party_state_id = cursor.lastrowid
        party_state = self.selectPartyStateById(party_state_id)
        return party_state
    
    def updatePartyState(self, body, party_state_id):
        query = 'UPDATE PartyState SET CustomerReference = ? WHERE PartyStateId = ?'
        _execute_query(query, (body.get('CustomerReference'), party_state_id,), commit=True)
        party_state = self.selectPartyStateById(party_state_id)
        return party_state