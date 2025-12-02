--
-- PostgreSQL database dump
--

\restrict rz75ZJ81Ziw7TkAWhvtITxRMEXFlxst50tIRzjxrNeBpYL6RCrmiSeQ3W7uhG6g

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: scms_admin
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
114	pbkdf2_sha256$600000$2MHPHlDBOQDypRBFmUXRrf$6fxNGPLWJA668y7wplw8hNB0AMDulDOflAekSd+cJU0=	\N	f	keyadash	Keya	Dash	keyadash@sample.org	t	t	2025-12-01 11:34:06.495849+00
115	pbkdf2_sha256$600000$w58u8NxB0GWcDplAJZHeoA$1HbFmN6dtdAaZtQHYbkezp1DP50EweKhcHcH7azVaK0=	\N	f	ranbirkota	Ranbir	Kota	ranbirkota@demo.edu	t	t	2025-12-01 11:34:06.836436+00
116	pbkdf2_sha256$600000$0S5naRPpXiJUUjwefYQ4hs$45IdiwGMM26BINlupc9jwFwRbxbUAO6ltB5vL5qWTjE=	\N	f	ojaschander	Ojas	Chander	ojaschander@demo.edu	t	t	2025-12-01 11:34:07.054259+00
117	pbkdf2_sha256$600000$n8DcYxSTcRTdOcjCUo5ibM$qNnFhgoBEDjDWTunk4jnrTlagT55YrClWinPn8JFuwA=	\N	f	aarnavarughese	Aarna	Varughese	aarnavarughese@demo.edu	t	t	2025-12-01 11:34:07.27193+00
118	pbkdf2_sha256$600000$GoT3gmaqrFTpNOGB2LPwvv$MLrTz+LBNP7Ac/9l40yfuF0cj+BXVtaXgbhcrFr8YgA=	\N	f	deepagaba	Deepa	Gaba	deepagaba@sample.org	t	t	2025-12-01 11:34:07.501859+00
119	pbkdf2_sha256$600000$GL98y2vDnRrSi6ymrR0MgC$OErmywqkNj+PQ7/zNeMg36E9MnKodTLdv6rn2xwcY6g=	\N	f	lavanyagoda	Lavanya	Goda	lavanyagoda@demo.edu	t	t	2025-12-01 11:34:07.72003+00
120	pbkdf2_sha256$600000$qvqQuiZgrOJHtbIqG674pc$aSyIhG7rpcRRzTX/R4UQdk+vK/jL11QgGzRTX0d8uUo=	\N	f	avideshmukh	Avi	Deshmukh	avideshmukh@example.com	t	t	2025-12-01 11:34:07.938649+00
121	pbkdf2_sha256$600000$zt6Ni8pxpilN6WHgIw6G0D$XLURm7DQuv1WJNpdBr+NUlb+Bf7se1tcIgz0WMS/ZBQ=	\N	f	charleschokshi	Charles	Chokshi	charleschokshi@test.local	t	t	2025-12-01 11:34:08.157271+00
122	pbkdf2_sha256$600000$rmCeEtRVLHWY0m95XzFZ4z$qUAOqJHSKVLpIxckHHtTpOHwmSFbdt/SkUWTr5SGIfw=	\N	f	alexandernatarajan	Alexander	Natarajan	alexandernatarajan@demo.edu	t	t	2025-12-01 11:34:08.386508+00
123	pbkdf2_sha256$600000$QfZztVLMHWWypnhzlwApLV$HE3Rp7hOKNz2GMtmSBRkwrIHTNwTmnVOF0Qbbt9I2vE=	\N	f	mitaliravel	Mitali	Ravel	mitaliravel@sample.org	t	t	2025-12-01 11:34:08.638748+00
124	pbkdf2_sha256$600000$MPz80lVzNIfc2VId4y0gO7$lHZpw1fwaf/bU8Phehff8sa3MfpiZVX7xi11VzVHDrU=	\N	f	abhaghosh	Abha	Ghosh	abhaghosh@demo.edu	f	t	2025-12-01 11:34:08.856864+00
125	pbkdf2_sha256$600000$sVPewZe1nLSIlY6TCNdUgY$ScN19NrrjLubDoqvgb++NWFdnLgKQiaogZWkUDLcHhY=	\N	f	triptigaba	Tripti	Gaba	triptigaba@demo.edu	f	t	2025-12-01 11:34:09.085646+00
126	pbkdf2_sha256$600000$vozAhQgLsWsGuHj6r8Ozwe$W4YLAg5shVNGz3HDrkvSyaTVPZlxWONQuqkUkGJnt98=	\N	f	darikakapur	Darika	Kapur	darikakapur@sample.org	f	t	2025-12-01 11:34:09.315454+00
127	pbkdf2_sha256$600000$jlUoqaQE5XsIQHup7voYMi$UC+h6kSXujZxFgpGjxyFSlK4qV5wgL9+/McQJZcddeU=	\N	f	zehaanbobal	Zehaan	Bobal	zehaanbobal@example.com	f	t	2025-12-01 11:34:09.656601+00
128	pbkdf2_sha256$600000$GUMewOTd6Strg4rI2xeENd$Ec6pNCx4BHnctsRxHXtt5clyd6XC0K6Hslb6JNyddTk=	\N	f	chamanbassi	Chaman	Bassi	chamanbassi@demo.edu	f	t	2025-12-01 11:34:09.894253+00
129	pbkdf2_sha256$600000$dUD0RHZaELWUFD8twCJ0uQ$I+H8TbYOUdV/gb4UfPNpoZlV1LMmj/gBkIqRMs0jKNA=	\N	f	vihaantak	Vihaan	Tak	vihaantak@demo.edu	f	t	2025-12-01 11:34:10.104064+00
130	pbkdf2_sha256$600000$NylpLQbWmX6TOvYxyXNSi9$M8bE2L4a1+2oi6zvLW5ylwkom5jJ1JSgSd0Ff0irdNA=	\N	f	chatreshoak	Chatresh	Oak	chatreshoak@test.local	f	t	2025-12-01 11:34:10.333198+00
131	pbkdf2_sha256$600000$Hc83aZvRQUQEDez3rfyPNy$0/vHntdmX2GSoWoYEkmywehSRmXlRrr7Bn5DqxDJTLk=	\N	f	yatandubey	Yatan	Dubey	yatandubey@example.com	f	t	2025-12-01 11:34:10.563473+00
132	pbkdf2_sha256$600000$lMdmi1Vr1coNSnTIDyhIoj$C68AsiPtrMP/i7p/rBp45Rh6AQ+40tTtWKwe2Mr8N0o=	\N	f	yashodababu	Yashoda	Babu	yashodababu@demo.edu	f	t	2025-12-01 11:34:10.792633+00
133	pbkdf2_sha256$600000$cXE1eK7bityQMzt9xljcHn$vyuNR5BCY8u3oCDzQAIZ62JgVUN+XdQHGsI6m9DyyKQ=	\N	f	adyahegde	Adya	Hegde	adyahegde@test.local	f	t	2025-12-01 11:34:11.42203+00
134	pbkdf2_sha256$600000$Fz69qLW7CzifCWyxPEqFhN$1jIr3iBR53dI4Gn49zCSDdPh5UKGMoKmISqWRJInrpI=	\N	f	radhakorpal	Radha	Korpal	radhakorpal@example.com	f	t	2025-12-01 11:34:11.665214+00
135	pbkdf2_sha256$600000$T2wD9pV9uiCUDwm4enZ9bU$SxiFBK07RRkqLE0wyVkke1VNe1rv4WGFQpGeU/fG5+M=	\N	f	dayitamani	Dayita	Mani	dayitamani@sample.org	f	t	2025-12-01 11:34:11.894781+00
136	pbkdf2_sha256$600000$D1QUy7MgMtlp2DAF1L8kyi$2BoDDwNY5ULF1iTmHVf6HSdtd9F+96Q0dzmG2SjAm7k=	\N	f	reyanshdeo	Reyansh	Deo	reyanshdeo@demo.edu	f	t	2025-12-01 11:34:12.123705+00
137	pbkdf2_sha256$600000$M2oQjekR5H6puYtlJ2zbeh$ppsc0hB4zZZIgphKrMyRbotQ9sOhTt+uMYEmvpZEC64=	\N	f	wrideshmanne	Wridesh	Manne	wrideshmanne@example.com	f	t	2025-12-01 11:34:12.342161+00
138	pbkdf2_sha256$600000$Qrt09YBbgfHcsDccqTQUGr$nYQT3aCSK7rTGr/NChHFiBHLwUAE4fEDtxfzIbnKqjA=	\N	f	vasudharatta	Vasudha	Ratta	vasudharatta@example.com	f	t	2025-12-01 11:34:12.560562+00
139	pbkdf2_sha256$600000$hDmS7tSNVd8Oldj6yLrKrI$XOdF80EUb1abUxCxBpMjlsw1sXpgfs01qkRFTiqhUEY=	\N	f	yashvigrewal	Yashvi	Grewal	yashvigrewal@demo.edu	f	t	2025-12-01 11:34:12.790383+00
140	pbkdf2_sha256$600000$9eqvVIJszOn0CsTawZ4mTd$iZiMF1uW+TjsrNVYjRIWOt05gCiHqBT7/8Qrxh1TNSI=	\N	f	nidrachowdhury	Nidra	Chowdhury	nidrachowdhury@example.com	f	t	2025-12-01 11:34:13.018834+00
141	pbkdf2_sha256$600000$WFdV883ga4xw9J8vNkfLcP$nf9KY7VXVt3/s7/OFYukxBbwCckelFzV79qTGV5jGvg=	\N	f	pranitpandit	Pranit	Pandit	pranitpandit@example.com	f	t	2025-12-01 11:34:13.259882+00
142	pbkdf2_sha256$600000$Qc4DwIrumEXtfvatolQeCb$FuIw8QwxK1y//Do0oLwHZmKpPAJrqct6QPKeyc4KdIU=	\N	f	jackgour	Jack	Gour	jackgour@test.local	f	t	2025-12-01 11:34:13.500461+00
143	pbkdf2_sha256$600000$6xnnvKFlVg6dhSGxSx8gFr$qYA2ToyWyqwqY1aCyJ0Y6YyJ4UVilS+YfvJWm+0en2s=	\N	f	pallaviram	Pallavi	Ram	pallaviram@demo.edu	f	t	2025-12-01 11:34:13.843611+00
144	pbkdf2_sha256$600000$nm58SSvjoZeYj7ebPWOI4V$L3TunxfDauvc3jL4RMnlPmkEPyh6r+S0+QJKhnfvA7Q=	\N	f	tanishmitra	Tanish	Mitra	tanishmitra@sample.org	f	t	2025-12-01 11:34:14.26503+00
145	pbkdf2_sha256$600000$z4PBmMYAfn8j9mo1zEg9pp$vW0QEzAItMXcT/Yj+7gr6o/h2odfLNKeXhUxIZFbf30=	\N	f	pranavchahal	Pranav	Chahal	pranavchahal@demo.edu	f	t	2025-12-01 11:34:14.505149+00
146	pbkdf2_sha256$600000$ik8I0eEJaMTLjLij4A8xJ6$0n4NcB0YBMaVfmGeQrHMYQrrDSl3EFZG+IIDRxxHXGE=	\N	f	tristantailor	Tristan	Tailor	tristantailor@test.local	f	t	2025-12-01 11:34:14.734773+00
147	pbkdf2_sha256$600000$R0N8ocAFk7h46iSntxcbPl$o7myzQZ/LuGD5kyHrd3dHU6PP1hnR5zZpHeXvLyRzVQ=	\N	f	orinderwable	Orinder	Wable	orinderwable@demo.edu	f	t	2025-12-01 11:34:15.030935+00
148	pbkdf2_sha256$600000$aruyyCfSzTKxoitVSlf3Ri$GvmZn/gEXEbIW9EhntfJ63b/rtWxXp8t91BTTCBpk+E=	\N	f	aarinibajwa	Aarini	Bajwa	aarinibajwa@example.com	f	t	2025-12-01 11:34:15.269753+00
149	pbkdf2_sha256$600000$p5fEkOTFJMBQYYW0xtW68r$dFfyo/ozRsx2w91aLayRP7kz0+dABGmf/tNXJXNA9Fw=	\N	f	qasimray	Qasim	Ray	qasimray@test.local	f	t	2025-12-01 11:34:15.511674+00
150	pbkdf2_sha256$600000$M0Ec1L91LNHG4m3l91OLAZ$gTPppqxjmah0xIKmzRJxyi+wpGGbRk1vHKuPP6v2dt0=	\N	f	raghavmaster	Raghav	Master	raghavmaster@test.local	f	t	2025-12-01 11:34:15.762739+00
151	pbkdf2_sha256$600000$5OXduvpbkBolCWIVUBov3B$Nyzg+ePkDjKRygIEppBknhUXRe6IxCeTFAm27jydD4U=	\N	f	aarinidatta	Aarini	Datta	aarinidatta@sample.org	f	t	2025-12-01 11:34:16.017113+00
152	pbkdf2_sha256$600000$N1LtZmXrrlZuEc2fYRYb5M$PZ3KxQEiNjgiWOyzWSI75sLCnTE3aemrf8CCZByPGTY=	\N	f	reyanshbabu	Reyansh	Babu	reyanshbabu@demo.edu	f	t	2025-12-01 11:34:16.247403+00
153	pbkdf2_sha256$600000$Azutr91xj4EmROg1CTJOrs$yZvoJ5dT12j7LHwHRl2zol3laqP2BLJ19VbIuG58vyU=	\N	f	ekantikahanda	Ekantika	Handa	ekantikahanda@sample.org	f	t	2025-12-01 11:34:16.498617+00
154	pbkdf2_sha256$600000$vgB06ki12xnFFoKej0WGKP$GV20ibMoB2e9o0iD0W0tewD8emP1qDtIN9j/vByPqbk=	\N	f	banjeetlal	Banjeet	Lal	banjeetlal@example.com	f	t	2025-12-01 11:34:16.75014+00
155	pbkdf2_sha256$600000$LTRsAJn1HyFv1ta8bAhqte$SOiumuSknA1W4CECaVeBPKnydpCYIcJSemLGF2qUutk=	\N	f	falakyohannan	Falak	Yohannan	falakyohannan@sample.org	f	t	2025-12-01 11:34:17.002734+00
156	pbkdf2_sha256$600000$HIBrMgfn3T9QLaHPkfbdWc$Dyx6V5OOxE6450mZh7jQmTJro5jmduW3553A8R5x10Y=	\N	f	ishitakhosla	Ishita	Khosla	ishitakhosla@sample.org	f	t	2025-12-01 11:34:17.253964+00
157	pbkdf2_sha256$600000$Oxzi5dLkdKQkLZuEhhb1yt$LA2AWHHFreS6qi3CIDOywvR2oZgAokgKrsbeCoXDhys=	\N	f	zayanratti	Zayan	Ratti	zayanratti@example.com	f	t	2025-12-01 11:34:17.549884+00
158	pbkdf2_sha256$600000$I4d8oKoAsGLOlIIHCCzZa9$UaHefLbXmnIis9HrjRBwmYsihJQa7WzOEVj2Va6+5gw=	\N	f	fradodeol	Frado	Deol	fradodeol@sample.org	f	t	2025-12-01 11:34:17.790858+00
159	pbkdf2_sha256$600000$PAmnHeL997Dmp2dAZ2NLBf$+YoTOWkKwzN3vcNfBlBfAoW/AUIb7eSqgx8J+o2nvfA=	\N	f	daminilala	Damini	Lala	daminilala@test.local	f	t	2025-12-01 11:34:18.052724+00
160	pbkdf2_sha256$600000$GwFY2ksnBTk6VB5sU6zF7I$vmZzLmrbexjRVAdUW4FZ9fTDFXhQxelp6pJByS56Qb4=	\N	f	chandreshvarghese	Chandresh	Varghese	chandreshvarghese@test.local	f	t	2025-12-01 11:34:18.270076+00
161	pbkdf2_sha256$600000$7T6YStRxjj15W9FH9YGYL5$d6Irq3UNAAA9rhramV03H3WHo1IYxCaO6nPvF97mWCM=	\N	f	tanmayibhatia	Tanmayi	Bhatia	tanmayibhatia@example.com	f	t	2025-12-01 11:34:18.489748+00
162	pbkdf2_sha256$600000$KCZWoYhkGw2n9kX2t2EAkK$t0rDcI9T9Y+/Kdh/3wc75jHHV2LaQcZ3hC2j804mgO4=	\N	f	agastyawadhwa	Agastya	Wadhwa	agastyawadhwa@example.com	f	t	2025-12-01 11:34:18.706768+00
163	pbkdf2_sha256$600000$cgaX2TzGV0bfY33EusBcRA$gi7B81Pc0J9oxfk/P87Ti/5eTbKMAfYR+axbIp2kMwE=	\N	f	faraspall	Faras	Pall	faraspall@test.local	f	t	2025-12-01 11:34:18.926143+00
164	pbkdf2_sha256$600000$3gVqAl1f7qFVsGLQcGwFFf$xiu0OL2jw6SRAhOIWKp+AZRyd8CAMGFW+ayVi++2Aag=	\N	f	aarnachar	Aarna	Char	aarnachar@demo.edu	f	t	2025-12-01 11:34:19.231078+00
165	pbkdf2_sha256$600000$kModwT7ff98ad2TYzvNJEP$AnAR2k7tZdQ9rFAABrjmJ+LPizqhAbXr7xhxliRGxs8=	\N	f	jonathanpurohit	Jonathan	Purohit	jonathanpurohit@example.com	f	t	2025-12-01 11:34:19.46325+00
166	pbkdf2_sha256$600000$PVmM6LwE5CIcSlB6zaG0O0$pkQi+NUQrg0MaxhzFcXmi49zOt1JdU2KvES+uvTdnKk=	\N	f	parthissac	Parth	Issac	parthissac@sample.org	f	t	2025-12-01 11:34:19.692046+00
167	pbkdf2_sha256$600000$sXTAARBiKvdDZwR8QbMZdY$yiB6G9ljQKctLyPEWcZcSDmlJZVDkZulPSJ/dBsXDpE=	\N	f	yochanabali	Yochana	Bali	yochanabali@example.com	f	t	2025-12-01 11:34:20.070567+00
168	pbkdf2_sha256$600000$kjwXb7VBfQg18n9KohXdix$RoCAQqDuQtjiQWajo2nHMnzt43SywnCFIDJfDEImH08=	\N	f	isaackrishnan	Isaac	Krishnan	isaackrishnan@example.com	f	t	2025-12-01 11:34:20.502536+00
169	pbkdf2_sha256$600000$TSAUa8KOeY5yvyoRYb5cO6$/aDmVC6CKxVCrvlc3m0gfeUFYDMstPrEk1p39KpiBoU=	\N	f	azaangola	Azaan	Gola	azaangola@demo.edu	f	t	2025-12-01 11:34:20.720958+00
170	pbkdf2_sha256$600000$IdLncFJM2k5KzoZHfIBxj3$eRiI0OuV2w7fbYf5lvVm1sewERi0WTwn9SGE7nuk23s=	\N	f	haritabera	Harita	Bera	haritabera@demo.edu	f	t	2025-12-01 11:34:20.939375+00
171	pbkdf2_sha256$600000$vKgRxNfTKZwwcqgAbD0r15$p0RQQt6aC+q3hHKOUMUc9vsjSVcu/JW23dcProQO9p4=	\N	f	saisingh	Sai	Singh	saisingh@example.com	f	t	2025-12-01 11:34:21.158106+00
172	pbkdf2_sha256$600000$KNtHDqKnAYtkDIruueT0E2$55k7NqDSroye6ZnpFTla4BfCsrTr9768B4P7YFbVVn4=	\N	f	hemanginihari	Hemangini	Hari	hemanginihari@demo.edu	f	t	2025-12-01 11:34:21.376058+00
173	pbkdf2_sha256$600000$dlFTXLzux1GzsoVg5JOgFs$0RPkQ9juCcMG1Xtv0B38k9EDy9+ZL6n+7QKmL4e9/BI=	\N	f	dominicnanda	Dominic	Nanda	dominicnanda@demo.edu	f	t	2025-12-01 11:34:21.605321+00
174	pbkdf2_sha256$600000$gaI53DVAGenZ6xDu3acdcH$PIGqYQzrfHSGtZxi2hfW2o+gpV8FcQDs/tM7kLuQcQY=	\N	f	diyabalay	Diya	Balay	diyabalay@example.com	f	t	2025-12-01 11:34:21.83578+00
175	pbkdf2_sha256$600000$pVbkt8ewFVzLowN878dsvo$ASORGY9qVuCzuuFaqklRWPDIIiaKbxB1lUKrSFPJ1WA=	\N	f	rachitchand	Rachit	Chand	rachitchand@test.local	f	t	2025-12-01 11:34:22.064387+00
176	pbkdf2_sha256$600000$m5Zsq1pRLY79xWy23RxZY3$l/hvInPBsW7Ct9f3OeQPPoBUzVs/gHTyHvuJjdbyX8E=	\N	f	eesharadhakrishnan	Eesha	Radhakrishnan	eesharadhakrishnan@demo.edu	f	t	2025-12-01 11:34:22.371797+00
177	pbkdf2_sha256$600000$yDdzun8xszWFUG64ftnGlx$hHb/I+EUHcprmORN8QVY0uNoVcRUp+UtfZR8N1Zgq5g=	\N	f	gauribarad	Gauri	Barad	gauribarad@test.local	f	t	2025-12-01 11:34:22.60146+00
178	pbkdf2_sha256$600000$rRuWXhmu8fs1h0iqtduYmp$dfMU4x5ERBXsNSoIHROhjBafLF0vlcQ2nGzrPOpxpPw=	\N	f	meeranaidu	Meera	Naidu	meeranaidu@test.local	f	t	2025-12-01 11:34:22.830504+00
179	pbkdf2_sha256$600000$L0d2IszSozadYzyhTINtvb$uso0tunhCGpITMuTuG/iuqnXY3m9q0QyzmnZ0HN5+9k=	\N	f	nandinitiwari	Nandini	Tiwari	nandinitiwari@demo.edu	f	t	2025-12-01 11:34:23.048096+00
180	pbkdf2_sha256$600000$hgyHortRQcn7elVhGQ82ox$CW6Pi7quLnR9HZCZKaFT5UwRrczgqHpn6e9ndbGTeNg=	\N	f	vedasahni	Veda	Sahni	vedasahni@demo.edu	f	t	2025-12-01 11:34:23.255919+00
181	pbkdf2_sha256$600000$8dMlgb7c8zkpkyPEfhTdam$k8ap4yJMtokBuA2NZksfaQV9hPsg9/wY47TwMqBVyzQ=	\N	f	maanasgoel	Maanas	Goel	maanasgoel@example.com	f	t	2025-12-01 11:34:23.474321+00
182	pbkdf2_sha256$600000$BSSHyt9MQBCQ1r2D2HMU9D$RqfhI1TsEC09OKSfXm8ttvfRUrAaBMCIzIKcrUpZxb8=	\N	f	masonmand	Mason	Mand	masonmand@demo.edu	f	t	2025-12-01 11:34:23.692522+00
183	pbkdf2_sha256$600000$4x0igu24iaabGaRUGBmLlV$b9O+yobB+z9nnTHKZAgLccu5M1r4EzOphQYd8C94jxs=	\N	f	radhikachaudhuri	Radhika	Chaudhuri	radhikachaudhuri@sample.org	f	t	2025-12-01 11:34:23.910091+00
184	pbkdf2_sha256$600000$oB0D2rfEi421obk0T3qPh1$w+pMwPae2f5xEOCO75xC+gej+slJvvYZFl2LGys7eJw=	\N	f	jagratireddy	Jagrati	Reddy	jagratireddy@example.com	f	t	2025-12-01 11:34:24.129117+00
185	pbkdf2_sha256$600000$PkzyhjW34wI9REk58oVYah$dlqJLraqjMgZk5M9bKjdSN1h+mNintQWXHVXuhcdPNQ=	\N	f	aarnamall	Aarna	Mall	aarnamall@demo.edu	f	t	2025-12-01 11:34:24.347309+00
186	pbkdf2_sha256$600000$el4Xi1DbLz22rEDpknWpZv$Im9enmwU8erBcQIBeiM6TAVnBFDS7xWmwzMBAdxlip4=	\N	f	daksheshkonda	Dakshesh	Konda	daksheshkonda@example.com	f	t	2025-12-01 11:34:24.566219+00
187	pbkdf2_sha256$600000$HvW55NGVWNQMU1ZR3TCE80$aVh5kJ6RrJyjCGA7Q6ASPlK6G6pp7kvRdmAayJM/uI8=	\N	f	gautamsabharwal	Gautam	Sabharwal	gautamsabharwal@demo.edu	f	t	2025-12-01 11:34:24.78429+00
188	pbkdf2_sha256$600000$60cRarCAFKmlMy0CFoEtEf$IG7OR3KVlfMDGD9OLun76G0zd5Cut/hx5kPyE8e8REQ=	\N	f	harshilgala	Harshil	Gala	harshilgala@test.local	f	t	2025-12-01 11:34:25.015727+00
189	pbkdf2_sha256$600000$sSoZRwrrF32uBYKPyOwQ3W$lAmyhhy0+e02+xs0ielVsCXMLWCgO7MhQXsapJSLDLE=	\N	f	yachanaraman	Yachana	Raman	yachanaraman@demo.edu	f	t	2025-12-01 11:34:25.298507+00
190	pbkdf2_sha256$600000$GNUt8YxfFil5puGzR0mP3v$0ezI9ep0MjNgco1HQrdUb0EQkGEYvBgL9Ii/kbLYS8k=	\N	f	samarchakraborty	Samar	Chakraborty	samarchakraborty@demo.edu	f	t	2025-12-01 11:34:25.629131+00
191	pbkdf2_sha256$600000$Pa6YosI0SsGAFuWmFaSJ5f$/EJyfaEgy7F64LMshWRVoHbwD6iTDqlO50JPq5nYN6k=	\N	f	bahadurjitranganathan	Bahadurjit	Ranganathan	bahadurjitranganathan@test.local	f	t	2025-12-01 11:34:25.867552+00
192	pbkdf2_sha256$600000$et0c9KSLJ8PdGuF1q9Lwsn$5pkoQJcJcSSudwQAUNXBQm3nYdQdm/HgSNkl1Yc5OBI=	\N	f	netrabhandari	Netra	Bhandari	netrabhandari@sample.org	f	t	2025-12-01 11:34:26.401952+00
193	pbkdf2_sha256$600000$O1xXfvBpOHC3UOl0FCXYRQ$0/ugSa8PP03RerwKPTwJ0j2EQV1HoyG2XwLytcvW0uc=	\N	f	falakarora	Falak	Arora	falakarora@example.com	f	t	2025-12-01 11:34:26.632555+00
194	pbkdf2_sha256$600000$k08rI1DlYFFrBi0a7XrjJA$8MYqHhog5YJPJC0I0SCQQQkHUf/mrmVSKunOASvyOEY=	\N	f	farhanboase	Farhan	Boase	farhanboase@sample.org	f	t	2025-12-01 11:34:26.851024+00
195	pbkdf2_sha256$600000$8YdTqBsLk13EeLIrBNwPl8$pBwrOkLlljM9oW2UCKmzklKballGX4oPE+Qt2mPimv8=	\N	f	labangupta	Laban	Gupta	labangupta@sample.org	f	t	2025-12-01 11:34:27.068461+00
196	pbkdf2_sha256$600000$E3ldOpoROp0mx3824SNkh7$Ddwl2/AHsvbYkUB33k0Fim3KJbvrBcaYbMZO48OBhh8=	\N	f	qasimmaster	Qasim	Master	qasimmaster@demo.edu	f	t	2025-12-01 11:34:27.287494+00
197	pbkdf2_sha256$600000$S8OCimw4cQPeA5pgFtzLQz$WxdZQQfeRr3Bkbgm3WmwqCTT1w1lYx8IAF6IzGlc9no=	\N	f	oeshigoel	Oeshi	Goel	oeshigoel@demo.edu	f	t	2025-12-01 11:34:27.50606+00
198	pbkdf2_sha256$600000$NRrY5VaoeQCiVBPjpgNirJ$sszyS+L0WgLDDbvYgKAJ984jdGRU+bEbm5GdmSjhEW4=	\N	f	wazirjohal	Wazir	Johal	wazirjohal@example.com	f	t	2025-12-01 11:34:27.802333+00
199	pbkdf2_sha256$600000$P7ACQoHohffAyxA2pc5APb$n7i1YZWGpcnAdpGo/7YUvW2q5lj5BOQKZk0aYOiX9yY=	\N	f	bhavikakata	Bhavika	Kata	bhavikakata@example.com	f	t	2025-12-01 11:34:28.021034+00
200	pbkdf2_sha256$600000$8w8zhbHElW4YbbCO0G6TZL$IXJJPR8H+JcvNLEbsLD3/vNVd7OsNqrzx88uRem7aI4=	\N	f	qarinbassi	Qarin	Bassi	qarinbassi@demo.edu	f	t	2025-12-01 11:34:28.24092+00
201	pbkdf2_sha256$600000$AQjUG2sjXIM9INahwALDOI$34cZY9OYpGtHBzeb+BoIVHZRQ6sUPEQRWmrD8awVAGc=	\N	f	ayushsibal	Ayush	Sibal	ayushsibal@example.com	f	t	2025-12-01 11:34:28.459193+00
202	pbkdf2_sha256$600000$lQcn93OHbvrxPiBDk4PV8G$rnFdFwLfxK16KEqdKIoNxATWpSWhf2g5VSl/Oily+8U=	\N	f	riyasaini	Riya	Saini	riyasaini@test.local	f	t	2025-12-01 11:34:28.677652+00
203	pbkdf2_sha256$600000$G1aO8UBEcdHpEm19xpwWlA$a1H7nb3VyhXq98EJyFq7xTpqBlmt2lS243fxX9hrJLw=	\N	f	radhikaramachandran	Radhika	Ramachandran	radhikaramachandran@test.local	f	t	2025-12-01 11:34:28.895403+00
204	pbkdf2_sha256$600000$MGU3XE7xJSjfGtSEdVuiz9$OiNNtx6wfO4RiOJicJC5zczwqPiNRDnLy4eb/6YluLs=	\N	f	jananidayal	Janani	Dayal	jananidayal@demo.edu	f	t	2025-12-01 11:34:29.114293+00
205	pbkdf2_sha256$600000$rEZ8aqKUHdh8SKKNY6pRfo$vnDtzeTYXyEYmTIDXn6oE5q3VLGRKPD74lmXVS0I5mQ=	\N	f	ikshitagrewal	Ikshita	Grewal	ikshitagrewal@sample.org	f	t	2025-12-01 11:34:29.332546+00
206	pbkdf2_sha256$600000$pJeKWA3MaN40dyxTNw6qzZ$MrcglKHr6+WNGY2E4BG6Nm805ZYs6BM/CRzCAVtloRY=	\N	f	yahvijaggi	Yahvi	Jaggi	yahvijaggi@example.com	f	t	2025-12-01 11:34:29.550421+00
207	pbkdf2_sha256$600000$YVkMtQqPnngtDlYLDb8ol1$swtygOOVm0S2dvLvTotWR5QwsxwCHgQPN6cJY8SZXqE=	\N	f	qabilchaudhary	Qabil	Chaudhary	qabilchaudhary@demo.edu	f	t	2025-12-01 11:34:29.769595+00
208	pbkdf2_sha256$600000$IE6gF2HXAMFBk55NrviB4S$VdX9PASAyXiWGMV6Rr0K674cdCfdXSobl/5HNTJXcGs=	\N	f	aryanchokshi	Aryan	Chokshi	aryanchokshi@sample.org	f	t	2025-12-01 11:34:29.998874+00
209	pbkdf2_sha256$600000$kl9qq6sRsibe1LaaeWLYEL$DxwcN0EtuSBaSkkfwHqzrc8bCy1EbH+U2HD41XD8da4=	\N	f	ikshitachad	Ikshita	Chad	ikshitachad@example.com	f	t	2025-12-01 11:34:30.228526+00
210	pbkdf2_sha256$600000$9iCMMNK8ZlwQe7vLN8vZtX$+Dn2WP+t4zXlid2B2lCr/xdntgO349I9cNTERAUpdHQ=	\N	f	tanaytalwar	Tanay	Talwar	tanaytalwar@example.com	f	t	2025-12-01 11:34:30.446961+00
211	pbkdf2_sha256$600000$W0frykwDy4FsFb0wTI0Gpw$CzApb4TMhks5+jnDjn0mxEgM3jvN6ocwZLMXUkIj/Zk=	\N	f	theodoreradhakrishnan	Theodore	Radhakrishnan	theodoreradhakrishnan@test.local	f	t	2025-12-01 11:34:30.761276+00
224	pbkdf2_sha256$600000$5WSWk1A7v3f4DquEHhh6PK$bRyUMP+gcy/3KNPA7XN/rBQlp/jgSVE2G8HLFyEgtg8=	2025-12-02 05:30:37.195573+00	t	sahil				t	t	2025-12-02 05:26:25+00
212	pbkdf2_sha256$600000$XTdoGDpde1IENczkFptGo8$ZdoBS/9lhfASdSzHH3po6UR+VJZhpjpcIwh9N8a6ZHg=	\N	f	xalaksarraf	Xalak	Sarraf	xalaksarraf@example.com	f	t	2025-12-01 11:34:31.0054+00
213	pbkdf2_sha256$600000$wpKmkAdr8xFAPTYvPAko9p$6O7on6lxm5Wd4djvs/ZgtIskizU8D5QD6pENZBzF7pc=	\N	f	snehashanker	Sneha	Shanker	snehashanker@test.local	f	t	2025-12-01 11:34:31.224307+00
214	pbkdf2_sha256$600000$6SZ24yBsVNQjxnb71YmdFt$hlsBMu7QECgBRi0aJ1kOXlLIEJxCvXMblxT+8pO/t/o=	\N	f	baljiwansood	Baljiwan	Sood	baljiwansood@example.com	f	t	2025-12-01 11:34:31.453739+00
215	pbkdf2_sha256$600000$auOYVIJ5KbLNPov9Y2TZz0$FAiKCQvrmBeHJJ+dsbzDWhNDrodfMJCxGJwJRHx42X0=	\N	f	raaginiram	Raagini	Ram	raaginiram@test.local	f	t	2025-12-01 11:34:31.816595+00
216	pbkdf2_sha256$600000$5uvVM3zZVlXCbCogEIsYxH$mCQAKCnRBxtEPTzjt7v5jUFTzkkBo6bKHbQlBjoxFUY=	\N	f	devanshrajan	Devansh	Rajan	devanshrajan@example.com	f	t	2025-12-01 11:34:32.04518+00
217	pbkdf2_sha256$600000$8zUT6jLSftnYtgnorfPGR4$OA6y1IBhPkfflahFW3rbkcrcQe+89NvkXE1IlkkppFI=	\N	f	rianatt	Ria	Natt	rianatt@example.com	f	t	2025-12-01 11:34:32.261629+00
218	pbkdf2_sha256$600000$R37OSiQmEMEbuL28hV3Pb0$NoXTwCUoiH8Zg7bzZDMhOZVu+FiNidsuie1aR7YjkmQ=	\N	f	dhruvchaudhari	Dhruv	Chaudhari	dhruvchaudhari@test.local	f	t	2025-12-01 11:34:32.482668+00
219	pbkdf2_sha256$600000$ofojIIPN6fNgUH4SROL0wb$N5fGRIaDAA5zat9HI3nvHzVJpj5O53G2L59uYQ3p86o=	\N	f	onkarnazareth	Onkar	Nazareth	onkarnazareth@demo.edu	f	t	2025-12-01 11:34:32.723051+00
220	pbkdf2_sha256$600000$EZXLQJQXJkxdGcF2sJqH59$Do7u0hLw8MVWBGTwCeJziDMhXby/JdR2lSCarAAgyfc=	\N	f	urishillawalia	Urishilla	Walia	urishillawalia@sample.org	f	t	2025-12-01 11:34:32.941613+00
221	pbkdf2_sha256$600000$7SVmMsAx25ljjgWUzvyESE$EZofWxVwtLpDgFyvJsXN+J21pD2eTu7KsjkN9QI0XuU=	\N	f	mugdhasekhon	Mugdha	Sekhon	mugdhasekhon@test.local	f	t	2025-12-01 11:34:33.170524+00
222	pbkdf2_sha256$600000$nbkZMzbIilAtUvzmMYhnKq$owTrA5n+S8xDWQLRxQj8pvJExBd/zFZrcaDhvVL4FlI=	\N	f	upkaarganesh	Upkaar	Ganesh	upkaarganesh@demo.edu	f	t	2025-12-01 11:34:33.389333+00
223	pbkdf2_sha256$600000$jBxxyUigr1nGNpm6QlXAse$eDvhILcqWjB+88UP6ocKzJYjn/mN20br5EUEETqr0lY=	\N	f	prishagade	Prisha	Gade	prishagade@sample.org	f	t	2025-12-01 11:34:33.619123+00
225	pbkdf2_sha256$600000$lvQBMo2OEYwi8DyynuAzrL$axVHrFUNDqKgRhvmQoQEjpnhNr3bp90NG9lPYTBQhKA=	\N	t	admin				t	t	2025-12-02 05:30:57+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: scms_admin
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
111	114	3
112	115	3
113	116	3
114	117	3
115	118	3
116	119	3
117	120	3
118	121	3
119	122	3
120	123	3
121	124	4
122	125	4
123	126	4
124	127	4
125	128	4
126	129	4
127	130	4
128	131	4
129	132	4
130	133	4
131	134	4
132	135	4
133	136	4
134	137	4
135	138	4
136	139	4
137	140	4
138	141	4
139	142	4
140	143	4
141	144	4
142	145	4
143	146	4
144	147	4
145	148	4
146	149	4
147	150	4
148	151	4
149	152	4
150	153	4
151	154	4
152	155	4
153	156	4
154	157	4
155	158	4
156	159	4
157	160	4
158	161	4
159	162	4
160	163	4
161	164	4
162	165	4
163	166	4
164	167	4
165	168	4
166	169	4
167	170	4
168	171	4
169	172	4
170	173	4
171	174	4
172	175	4
173	176	4
174	177	4
175	178	4
176	179	4
177	180	4
178	181	4
179	182	4
180	183	4
181	184	4
182	185	4
183	186	4
184	187	4
185	188	4
186	189	4
187	190	4
188	191	4
189	192	4
190	193	4
191	194	4
192	195	4
193	196	4
194	197	4
195	198	4
196	199	4
197	200	4
198	201	4
199	202	4
200	203	4
201	204	4
202	205	4
203	206	4
204	207	4
205	208	4
206	209	4
207	210	4
208	211	4
209	212	4
210	213	4
211	214	4
212	215	4
213	216	4
214	217	4
215	218	4
216	219	4
217	220	4
218	221	4
219	222	4
220	223	4
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: scms_admin
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scms_admin
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 220, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scms_admin
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 225, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scms_admin
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict rz75ZJ81Ziw7TkAWhvtITxRMEXFlxst50tIRzjxrNeBpYL6RCrmiSeQ3W7uhG6g

