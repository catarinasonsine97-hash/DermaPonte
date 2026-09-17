package br.com.dermaponte.triage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PriorityServiceTest {
    private final PriorityService service = new PriorityService();
    @Test void noReportedSignsIsRoutineButNotADiagnosis() {
        var result = service.assess(new PriorityService.Questionnaire(false,false,false,false,false,false));
        assertEquals("ROUTINE", result.priority());
        assertEquals(0, result.score());
        assertTrue(result.disclaimer().contains("Não é diagnóstico"));
    }
    @Test void scoreThreeIsSoon() {
        assertEquals("SOON", service.assess(new PriorityService.Questionnaire(true,false,false,false,false,false)).priority());
    }
    @Test void scoreSixIsUrgentAndExplained() {
        var result = service.assess(new PriorityService.Questionnaire(true,true,false,false,false,false));
        assertEquals("URGENT", result.priority());
        assertEquals(6, result.score());
        assertEquals(2, result.reasons().size());
    }
    @Test void allReportedSignsScoreFifteen() {
        assertEquals(15, service.assess(new PriorityService.Questionnaire(true,true,true,true,true,true)).score());
    }
}
