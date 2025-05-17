% STR: Condição da rua (multivalorada)
0.6::str(dry); 0.3::str(wet); 0.1::str(snow_covered).

% FLW: Volante desgastado
0.1::flw.
% B: Lâmpada ok
0.95::b.
% K: Cabo ok
0.97::k.

% R: Dínamo deslizante
0.15::r.

% V depende apenas de R (V ⫫ Flw, Str | R)
0.2::v :- r.           % Dínamo está deslizando → baixa chance de gerar tensão
0.95::v :- \+r.        % Dínamo normal → alta chance de gerar tensão

% Li (luz ligada) depende de V, B, K via CPT fornecida

% V = true cases
0.99::li :- v, b, k.
0.01::li :- v, b, \+k.
0.01::li :- v, \+b, k.
0.001::li :- v, \+b, \+k.

% V = false cases
0.3::li :- \+v, b, k.
0.005::li :- \+v, b, \+k.
0.005::li :- \+v, \+b, k.
% No rule for (\+v, \+b, \+k) → implicit 0 probability

% Evidência: a condição da rua é snow_covered
evidence(str(snow_covered)).

% Consulta: qual a chance de que V esteja ativo (tensão gerada)?
query(v).