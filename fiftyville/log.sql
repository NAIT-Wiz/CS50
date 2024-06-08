--Check crime scene reports for Humphrey street
SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Check all interviews
SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

--Final surfing  relavant interviews with transcript that matches discription of crime scene reports.
SELECT *
FROM interviews
WHERE (name = 'Ruth' OR name = 'Eugene' OR name = 'Raymond')
AND year = 2023
AND month = 7
AND day = 28;

--Checking bank account numbers and names with atm withdrawals at Leggett Streeton 28 July 2028
SELECT atm.account_number, atm.transaction_type, atm.atm_location, atm.amount, ba.person_id, p.name
FROM atm_transactions atm
JOIN bank_accounts ba ON atm.account_number = ba.account_number
JOIN people p ON ba.person_id = p.id
WHERE atm.year = 2023
AND atm.month = 7
AND atm.day = 28
AND atm.atm_location = 'Leggett Street'
AND atm.transaction_type = 'withdraw';

-- check names and numbers that made and recieved calls on 28 JULY 2023
SELECT p1.name AS caller_name, p1.phone_number AS caller_phone, p1.passport_number AS caller_passport,
       p2.name AS receiver_name, p2.phone_number AS receiver_phone, p2.passport_number AS receiver_passport,
       pc.duration
FROM phone_calls pc
JOIN people p1 ON pc.caller = p1.phone_number
JOIN people p2 ON pc.receiver = p2.phone_number
WHERE pc.month = 7
  AND pc.day = 28
  AND pc.year = 2023
  AND pc.duration <= 60
ORDER BY caller_name;

-- Identify cars and car owner names from bakery lot driveway parking exit
SELECT bakery_security_logs.id,
       people.name,
       CONCAT(bakery_security_logs.year, '-', bakery_security_logs.month, '-', bakery_security_logs.day, ' ', bakery_security_logs.hour, ':', bakery_security_logs.minute) AS exit_time,
       bakery_security_logs.activity,
       bakery_security_logs.license_plate,
       people.phone_number,
       people.passport_number
FROM bakery_security_logs
LEFT JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE activity = 'exit'
AND bakery_security_logs.year = 2023
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 59;

--Identify  all airports in FIFTYVILLE
SELECT *
FROM airports
WHERE city = 'Fiftyville';

--Identify all flights leaving Fiftyville
SELECT airports.*,
       destination_airport.city AS destination_city,
       CONCAT(flights.year, '-', flights.month, '-', flights.day, ' ', flights.hour, ':', flights.minute) AS flight_departure
FROM airports
JOIN flights ON airports.id = flights.origin_airport_id
JOIN airports AS destination_airport ON flights.destination_airport_id = destination_airport.id
WHERE flights.year = 2023
AND flights.month = 7
AND ((flights.day = 28 AND flights.hour >= 10) OR (flights.day = 29 AND flights.hour < 10))
AND airports.full_name = 'Fiftyville Regional Airport';

--Identify passengers who left Fiftyville Regional Airport ON 28 OR 29 JULY
SELECT passengers.*, people.name AS passenger_name,
       CONCAT(flights.year, '-', flights.month, '-', flights.day, ' ', flights.hour, ':', flights.minute) AS flight_departure
FROM passengers
JOIN flights ON passengers.flight_id = flights.id
JOIN airports AS origin_airport ON flights.origin_airport_id = origin_airport.id
JOIN people ON passengers.passport_number = people.passport_number
WHERE origin_airport.full_name = 'Fiftyville Regional Airport'
AND ((flights.year = 2023 AND flights.month = 7 AND flights.day = 28 AND flights.hour >= 10 AND flights.minute >= 45)
OR (flights.year = 2023 AND flights.month = 7 AND flights.day = 29))
ORDER BY passenger_name;


--The name that appears on all sql series is Bruce so identfy flight details for Bruce
SELECT DISTINCT a.city AS destination_city,
                ppl.name AS passenger_name,
                ppl.passport_number AS passport_number,
                p.seat AS seat_number,
                ppl.phone_number AS phone_number,
                CONCAT(f.year, '-', f.month, '-', f.day, ' ', f.hour, ':', f.minute) AS departure_time
FROM passengers AS p
JOIN flights AS f ON p.flight_id = f.id
JOIN airports AS a ON f.destination_airport_id = a.id
JOIN people AS ppl ON p.passport_number = ppl.passport_number
WHERE ppl.name = 'Bruce';

---identfy his accomplice by quering the name of the (676) 555-6554 number called by Taylor, from the phone calls query
SELECT pc.caller AS caller_number, pc.receiver AS receiver_number, pc.duration,
       caller.name AS caller_name, caller.passport_number AS caller_passport,
       receiver.name AS receiver_name, receiver.passport_number AS receiver_passport
FROM phone_calls pc
JOIN people AS caller ON pc.caller = caller.phone_number
JOIN people AS receiver ON pc.receiver = receiver.phone_number
WHERE pc.receiver = '(676) 555-6554'
AND pc.year = 2023
AND pc.month = 7
AND pc.day = 28;
