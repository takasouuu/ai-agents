# 10 Data Model Logical

- エンティティ（REQ-004, REQ-008, REQ-009）: Requirement / DesignDocument / WorkflowExecution / Review / ReviewFinding / Traceability
- Requirement 1:N DesignDocument / Review / Traceability の関連を持つ
- 制約: requirement_id一意、traceabilityでrequirement_id必須、finding_id重複禁止
