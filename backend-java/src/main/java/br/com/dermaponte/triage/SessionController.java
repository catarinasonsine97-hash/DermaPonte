package br.com.dermaponte.triage;

import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SessionController {
    public record Token(String token, String headerName) {}

    @GetMapping("/api/v1/session/csrf")
    public Token csrf(CsrfToken token) {
        return new Token(token.getToken(), token.getHeaderName());
    }
}
