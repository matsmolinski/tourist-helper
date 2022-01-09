### tourist-helper
Tworzona przez nas usługa ma służyć do prostej i bezpiecznej analizy plików graficznych i PDF pod kątem wykrywania oraz analizy zawartego tekstu. Analiza zawartego tekstu będzie polegała na ewaluacji wydźwięku tekstu. Aplikacja będzie umożliwiała analizę tekstu w wybranym języku oraz jego tłumaczenie. Usługa będzie dostępna przez serwis webowy. Dostęp do aplikacji będzie możliwy na dwa sposoby:

- Po wysłaniu pliku do analizy użytkownik otrzyma powiadomienie w aplikacji, że analiza się rozpoczęła oraz, że po zakończeniu dostanie wiadomość email z kodem dostępu do analizy.
- Użytkownik będzie posiadał własne konto do którego będzie posiadał możliwość zalogowania. Po zalogowaniu użytkownikowi zostanie udostępniona możliwość wysłania nowego obrazu do analizy, ale również i możliwość wyświetlenia historycznych analiz.

## Diagram architektury
![picture](https://github.com/matsmolinski/tourist-helper/blob/main/architecture_diagram.svg)

## Diagram przypadków użycia
![picture](https://github.com/matsmolinski/tourist-helper/blob/main/Use%20case%20diagram.png)


## Technologie i narzędzia

Zewnętrzna warstwa czyli App Services, której zadaniem będzie umożliwienie komunikacji z użytkownikiem zaimplementowana zostanie w Pythonie.
Stworzony zostanie mikroserwis bazujący na bibliotece Flask oraz na frameworku Jinja2. Połączenie te umożliwi nam łatwe zbudowanie aplikacji webowej
oraz silnika templatek dzięki któremu będziemy mieli możliwość stworzyć prosty i przejrzysty interfejs graficzny.

App Services będzie udostępniał między innymi możliwość logowania już zarejestrowanych użytkowników. Do przechowywania danych logowania wykorzystana zostanie usługa
Azure Cache for Redis. W połączeniu z pythonową biblioteką PyRedis umożliwi utworzenie prostego mechanizmu autentykacji.

Function Apps, który stanowi rdzeń naszej aplikacji będzie zbudowany również w pythonie. Jego zadaniem będzie bezserwerowe przetworzenie zapytań przesyłanych przez użytkowników, a także komunikacja z serwisami kognitywnymi (poznawczymi) oraz usługami Logic Apps. 

## Prezentacja rozwiązania
W projekcie utworzona została aplikacja internetowa, która pozwala na tłumaczenia anonimowe oraz tłumaczenie powiązane z kontem użytkownika.

<img src="https://github.com/matsmolinski/tourist-helper/blob/main/mainPage.png" height="150">

Po każdym tłumaczeniu użytkownik jest informowany drogą mailową o zakończeniu tłumaczenia. Użytkownik otrzymuje link do odczytu wyników.

<img src="https://github.com/matsmolinski/tourist-helper/blob/main/email.png" height="150">

Zalogowani użytkownicy mogą w każdej chwili sprawdzić swoje wszystkie tłumaczenia.

<img src="https://github.com/matsmolinski/tourist-helper/blob/main/list.png" height="250">

Przykładowe wyniki tłumaczenia prezentują się następująco:

<img src="https://github.com/matsmolinski/tourist-helper/blob/main/result.png" height="250">
