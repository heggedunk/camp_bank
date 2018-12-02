INSERT INTO public."camper" (name, prompt) VALUES ('Jake Heggeland', 'SUP');
INSERT INTO public."camper" (name, prompt) VALUES ('Molly Fletchall', 'Yo');

INSERT INTO public."item" (item_desc, is_debit) VALUES  ('Deposit', FALSE);
INSERT INTO public."item" (item_desc) VALUES  ('Concessions');
INSERT INTO public."item" (item_desc) VALUES  ('Shirt Shack');
INSERT INTO public."item" (item_desc) VALUES  ('Withdrawal');

insert into public."session" (description, active) values ('Test-1', TRUE);
insert into public."session" (description) values ('Test-2');
insert into public."session" (description) values ('Test-3');
