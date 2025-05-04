:- dynamic gejala_pos/1.
:- dynamic gejala_neg/1.

% Fakta gangguan tidur
penyakit("Insomnia").
penyakit("Sleep Apnea").
penyakit("Narkolepsi").
penyakit("Restless Leg Syndrome").

% Gejala tiap penyakit
gejala(sulit_tidur, "Insomnia").
gejala(terbangun_tengah_malam, "Insomnia").
gejala(lelah_siang_hari, "Insomnia").

gejala(ngorok_keras, "Sleep Apnea").
gejala(sulit_bernapas_saat_tidur, "Sleep Apnea").
gejala(sakit_kepala_pagi, "Sleep Apnea").

gejala(sering_tertidur_tiba_tiba, "Narkolepsi").
gejala(halusinasi_saat_tidur, "Narkolepsi").
gejala(kelumpuhan_tidur, "Narkolepsi").

gejala(sensasi_gatal_kaki, "Restless Leg Syndrome").
gejala(gerakan_kaki_tak_sadar, "Restless Leg Syndrome").
gejala(sulit_tidur, "Restless Leg Syndrome").

% Pertanyaan
pertanyaan(sulit_tidur, "Apakah Anda mengalami kesulitan untuk tertidur?").
pertanyaan(terbangun_tengah_malam, "Apakah Anda sering terbangun di tengah malam?").
pertanyaan(lelah_siang_hari, "Apakah Anda merasa sangat lelah di siang hari?").
pertanyaan(ngorok_keras, "Apakah Anda mendengkur keras saat tidur?").
pertanyaan(sulit_bernapas_saat_tidur, "Apakah Anda merasa sulit bernapas saat tidur?").
pertanyaan(sakit_kepala_pagi, "Apakah Anda sering sakit kepala saat bangun pagi?").
pertanyaan(sering_tertidur_tiba_tiba, "Apakah Anda sering tertidur tiba-tiba?").
pertanyaan(halusinasi_saat_tidur, "Apakah Anda mengalami halusinasi saat tertidur atau bangun?").
pertanyaan(kelumpuhan_tidur, "Apakah Anda merasa lumpuh sesaat ketika bangun atau tertidur?").
pertanyaan(sensasi_gatal_kaki, "Apakah Anda merasakan sensasi gatal atau tak nyaman di kaki saat istirahat?").
pertanyaan(gerakan_kaki_tak_sadar, "Apakah kaki Anda bergerak tanpa disadari saat tidur?").

% Aturan Diagnosa
diagnosa(P) :-
    penyakit(P),
    findall(G, gejala(G, P), GejalaList),
    semua_gejala_positif(GejalaList).

semua_gejala_positif([]).
semua_gejala_positif([G|Rest]) :-
    gejala_pos(G),
    semua_gejala_positif(Rest).
