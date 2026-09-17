package br.com.dermaponte.triage;

import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

/** Educational rules only: not clinically validated, not an image diagnosis. */
@Service
public class PriorityService {
    public record Questionnaire(boolean changed, boolean bleeding, boolean itchingOrPain,
            boolean notHealing, boolean personalHistory, boolean familyHistory) {}
    public record Assessment(String priority, int score, List<String> reasons, String disclaimer) {}

    public Assessment assess(Questionnaire input) {
        int score = 0;
        List<String> reasons = new ArrayList<>();
        if (input.changed()) { score += 3; reasons.add("Mudança relatada na lesão"); }
        if (input.bleeding()) { score += 3; reasons.add("Sangramento relatado"); }
        if (input.itchingOrPain()) { score += 1; reasons.add("Coceira ou dor relatada"); }
        if (input.notHealing()) { score += 4; reasons.add("Ferida que não cicatriza relatada"); }
        if (input.personalHistory()) { score += 3; reasons.add("Histórico pessoal relatado"); }
        if (input.familyHistory()) { score += 1; reasons.add("Histórico familiar relatado"); }
        String priority = score >= 6 ? "URGENT" : score >= 3 ? "SOON" : "ROUTINE";
        return new Assessment(priority, score, List.copyOf(reasons),
                "Classificação demonstrativa, sem validação clínica. Não é diagnóstico nem exclui doença; requer avaliação médica.");
    }
}
