--
-- PostgreSQL database dump
--

\restrict TFC5mgweHnUiOqf4FXByvxwXjkGwvLEKuum9koA0n8pOB6Kd2U5QGaUa55b5h00

-- Dumped from database version 18.6 (Ubuntu 18.6-0ubuntu0.26.04.1)
-- Dumped by pg_dump version 18.6 (Ubuntu 18.6-0ubuntu0.26.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (6, 'core', 'dispositivo');
INSERT INTO public.django_content_type VALUES (7, 'core', 'user');
INSERT INTO public.django_content_type VALUES (8, 'core', 'funcionario');
INSERT INTO public.django_content_type VALUES (9, 'core', 'paciente');
INSERT INTO public.django_content_type VALUES (10, 'core', 'leitura');
INSERT INTO public.django_content_type VALUES (11, 'core', 'relatorio');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission VALUES (21, 'Can add Dispositivo', 6, 'add_dispositivo');
INSERT INTO public.auth_permission VALUES (22, 'Can change Dispositivo', 6, 'change_dispositivo');
INSERT INTO public.auth_permission VALUES (23, 'Can delete Dispositivo', 6, 'delete_dispositivo');
INSERT INTO public.auth_permission VALUES (24, 'Can view Dispositivo', 6, 'view_dispositivo');
INSERT INTO public.auth_permission VALUES (25, 'Can add Usuário', 7, 'add_user');
INSERT INTO public.auth_permission VALUES (26, 'Can change Usuário', 7, 'change_user');
INSERT INTO public.auth_permission VALUES (27, 'Can delete Usuário', 7, 'delete_user');
INSERT INTO public.auth_permission VALUES (28, 'Can view Usuário', 7, 'view_user');
INSERT INTO public.auth_permission VALUES (29, 'Can add Funcionário', 8, 'add_funcionario');
INSERT INTO public.auth_permission VALUES (30, 'Can change Funcionário', 8, 'change_funcionario');
INSERT INTO public.auth_permission VALUES (31, 'Can delete Funcionário', 8, 'delete_funcionario');
INSERT INTO public.auth_permission VALUES (32, 'Can view Funcionário', 8, 'view_funcionario');
INSERT INTO public.auth_permission VALUES (33, 'Can add Paciente', 9, 'add_paciente');
INSERT INTO public.auth_permission VALUES (34, 'Can change Paciente', 9, 'change_paciente');
INSERT INTO public.auth_permission VALUES (35, 'Can delete Paciente', 9, 'delete_paciente');
INSERT INTO public.auth_permission VALUES (36, 'Can view Paciente', 9, 'view_paciente');
INSERT INTO public.auth_permission VALUES (37, 'Can add Leitura', 10, 'add_leitura');
INSERT INTO public.auth_permission VALUES (38, 'Can change Leitura', 10, 'change_leitura');
INSERT INTO public.auth_permission VALUES (39, 'Can delete Leitura', 10, 'delete_leitura');
INSERT INTO public.auth_permission VALUES (40, 'Can view Leitura', 10, 'view_leitura');
INSERT INTO public.auth_permission VALUES (41, 'Can add Relatório', 11, 'add_relatorio');
INSERT INTO public.auth_permission VALUES (42, 'Can change Relatório', 11, 'change_relatorio');
INSERT INTO public.auth_permission VALUES (43, 'Can delete Relatório', 11, 'delete_relatorio');
INSERT INTO public.auth_permission VALUES (44, 'Can view Relatório', 11, 'view_relatorio');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_dispositivo; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_user; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--

INSERT INTO public.core_user VALUES (1, 'pbkdf2_sha256$1000000$RgS5wFSjythyQIHrfyvyjA$4YkLuVYT7SpR/LDL/sFP5fORPaY3xUuNqv36DeeRFCo=', NULL, true, 'admin', '', '', '', true, true, '2026-07-14 17:51:10.049438-03', '', 'PACIENTE', '', NULL, '');


--
-- Data for Name: core_funcionario; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_paciente; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_leitura; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_relatorio; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_relatorio_leituras; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_user_groups; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: core_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--

INSERT INTO public.django_migrations VALUES (1, 'contenttypes', '0001_initial', '2026-07-14 17:50:31.641496-03');
INSERT INTO public.django_migrations VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-07-14 17:50:31.649493-03');
INSERT INTO public.django_migrations VALUES (3, 'auth', '0001_initial', '2026-07-14 17:50:31.682677-03');
INSERT INTO public.django_migrations VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-07-14 17:50:31.688783-03');
INSERT INTO public.django_migrations VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-07-14 17:50:31.695269-03');
INSERT INTO public.django_migrations VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-07-14 17:50:31.701398-03');
INSERT INTO public.django_migrations VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-07-14 17:50:31.707604-03');
INSERT INTO public.django_migrations VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-07-14 17:50:31.710027-03');
INSERT INTO public.django_migrations VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-07-14 17:50:31.715999-03');
INSERT INTO public.django_migrations VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-07-14 17:50:31.722517-03');
INSERT INTO public.django_migrations VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-07-14 17:50:31.7295-03');
INSERT INTO public.django_migrations VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-07-14 17:50:31.743899-03');
INSERT INTO public.django_migrations VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-07-14 17:50:31.749446-03');
INSERT INTO public.django_migrations VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-07-14 17:50:31.755681-03');
INSERT INTO public.django_migrations VALUES (15, 'core', '0001_initial', '2026-07-14 17:50:31.871803-03');
INSERT INTO public.django_migrations VALUES (16, 'admin', '0001_initial', '2026-07-14 17:50:31.896887-03');
INSERT INTO public.django_migrations VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2026-07-14 17:50:31.906772-03');
INSERT INTO public.django_migrations VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2026-07-14 17:50:31.921631-03');
INSERT INTO public.django_migrations VALUES (19, 'sessions', '0001_initial', '2026-07-14 17:50:31.930951-03');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: prostatcare_user
--



--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 44, true);


--
-- Name: core_dispositivo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_dispositivo_id_seq', 1, false);


--
-- Name: core_funcionario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_funcionario_id_seq', 1, false);


--
-- Name: core_leitura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_leitura_id_seq', 1, false);


--
-- Name: core_paciente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_paciente_id_seq', 1, false);


--
-- Name: core_relatorio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_relatorio_id_seq', 1, false);


--
-- Name: core_relatorio_leituras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_relatorio_leituras_id_seq', 1, false);


--
-- Name: core_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_user_groups_id_seq', 1, false);


--
-- Name: core_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_user_id_seq', 1, true);


--
-- Name: core_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.core_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: prostatcare_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- PostgreSQL database dump complete
--

\unrestrict TFC5mgweHnUiOqf4FXByvxwXjkGwvLEKuum9koA0n8pOB6Kd2U5QGaUa55b5h00

