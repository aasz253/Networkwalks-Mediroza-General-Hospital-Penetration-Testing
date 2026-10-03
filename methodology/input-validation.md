# Procedure 4 — Input validation

Testing how untrusted input is handled, and where the application's trust decisions
fail.

> **Authorisation precondition.** Active input testing of in-scope parameters under
> written authorisation, bounded by agreed stopping conditions.

---

## 1. Core principle

**Validate at the boundary. Parameterise at the data layer. Encode at the output
layer.** Three different jobs, three different controls.

| Layer | Control | Purpose |
| --- | --- | --- |
| Boundary | Allow-list validation | Reject unacceptable input early, cheaply |
| Data layer | Parameterised queries / typed APIs | Make injection structurally impossible |
| Output | Contextual encoding | Prevent the data becoming markup or script |

> The engagement's Critical finding failed at the **data** layer. No amount of
> boundary filtering replaces parameterisation; it only moves the bypass problem.

---

## 2. Injection classes

| Class | Test input principle | Primary control |
| --- | --- | --- |
| SQL / database | A single metacharacter, then a terminator | Parameterisation |
| Command | Metacharacter in a value passed to a process | Avoid shell invocation; use argument arrays |
| Template | Expression delimiters in user-controlled template source | Do not build templates from user input |
| Path traversal | Relative path segments | Canonicalise and confine to an allowed base |
| Header | Newline characters | Validate and strip; never concatenate into headers |
| LDAP / NoSQL / XPath | Operator and structure characters | Parameterise for that data source |

### 2.1 The single-metacharacter first step

Testing begins with **one** character that should never appear in a value being
placed into a structured language.

| Observation | Conclusion |
| --- | --- |
| Input rejected cleanly | No signal; move to the next control |
| Input accepted and stored | Validation is absent — investigate the sink |
| Structured error returned | **Injection confirmed**, and the error reveals the sink's structure |

> In this engagement one quote produced a database syntax error that identified the
> driver, the engine, and the position of the injected input. One character was
> sufficient, and no exploitation tooling was involved.

---

## 3. Handling errors safely

| Rule | Reason |
| --- | --- |
| Read what the error returns; do not suppress it silently | The error is the primary evidence |
| Never send production-shaped data to a third-party service to interpret it | It becomes a disclosure event |
| Redact internal hostnames, paths and identifiers before publishing | They assist lateral movement |
| Note that verbose errors are dangerous **because** the endpoint is injectable | On a parameterised endpoint the same error is harmless |

---

## 4. The bypass mindset

Once a parameter is confirmed injectable, the question is not "can I read the
database" but "what does this input control?".

| Question | Answer in this engagement |
| --- | --- |
| Does it change the query's meaning? | Yes |
| Does it remove a security predicate? | **Yes — the password comparison** |
| Is further extraction necessary? | No. Impact is already proven |

> Deleting a check is a complete, demonstrable impact. Extraction beyond that point
> is not a stronger finding; it is only a larger data-handling problem.

---

## 5. Validation review

| Question | How to answer it | What to record |
| --- | --- | --- |
| Is validation server-side? | Attempt a client-side bypass by submitting directly | Whether client-side validation is the only control |
| Is it allow-list or deny-list? | Read the validation code, if available | Deny-list is a maintenance liability |
| Is it applied consistently? | Compare sibling endpoints | One validated endpoint proves nothing about the rest |
| Does it apply to every parameter? | Inventory parameters against validation points | Untested parameters as hypotheses |
| Is encoding applied at output? | Review the rendering context | Escaping in the wrong context is no escaping |

> **The consistency question is the one that matters most.** Validating one
> parameter on one endpoint is common and worthless. The engagement records that
> other entry points were **not** tested, rather than implying the validated one
> represents the codebase.

---

## 6. Reporting precision

| Wording | Meaning | Acceptable |
| --- | --- |
| "Confirmed injectable" | A structured error demonstrated it | ✅ |
| "The error identified the query structure" | Observation | ✅ |
| "Other parameters are probably injectable" | Hypothesis | ✅ if labelled |
| "The application is SQL-injectable" | Over-generalisation | ❌ |
| "No injection found elsewhere" | Only valid if every parameter was tested | ❌ unless true and evidenced |

---

## 7. Correct implementation

```php
// Deny-list — brittle, and still bypassable
$sql = "SELECT id FROM users WHERE role = '$role'";   // ❌

// Parameterisation — the primary control
$stmt = $db->prepare('SELECT id FROM users WHERE role = :role');
$stmt->execute([':role' => $validatedRole]);          // ✅

// Boundary validation — reduces noise, cannot replace parameterisation
$allowed = ['admin', 'staff', 'patient'];
if (!in_array($inputRole, $allowed, true)) {
    throw new InvalidArgumentException('Invalid role');
}

// Output encoding — contextual
htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
```

---

## 8. Excluded techniques

| Excluded | Reason |
| --- | --- |
| Automated fuzzing | Availability risk; unbounded requests |
| Exploitation frameworks | Unnecessary once a weakness is proven |
| Time-based blind injection | Slower, noisier, and adds nothing to a proven finding |
| Payload collections or generators | Out of scope; not published in this repository |
| Bulk parameter testing | Beyond the validation objective |

---

## 9. Retest criteria

| # | Criterion | Pass condition |
| --- | --- | --- |
| 1 | Injection removed from the confirmed parameter | No structured error on any input |
| 2 | Injection removed from sibling parameters | No structured error on any input |
| 3 | All queries parameterised at every call site | Code review; SAST reports no concatenation into a query API |
| 4 | Verbose errors disabled | No driver name, stack trace or SQL fragment returned |
| 5 | Validation allow-list and server-side | Direct request bypassing client validation is rejected |
| 6 | Output encoding correct for the context | Context-appropriate escaping at each sink |
| 7 | Detection in place | Repeated database errors alert |

---

## 10. Checklist

- [ ] Authorisation covers input testing; stopping conditions agreed
- [ ] Single-metacharacter step performed first
- [ ] Error content analysed and treated as evidence
- [ ] No third-party service used to interpret errors containing data
- [ ] Testing stopped once impact was substantiated
- [ ] Every parameter inventoried; untested ones recorded as hypotheses
- [ ] Correct implementation documented, not just the flaw
- [ ] Retest criteria observable and specific