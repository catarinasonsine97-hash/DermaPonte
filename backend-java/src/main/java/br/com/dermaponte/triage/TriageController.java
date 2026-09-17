package br.com.dermaponte.triage;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/triage")
public class TriageController {
    private final PriorityService service;
    public TriageController(PriorityService service) { this.service = service; }

    public record Request(@NotNull Boolean changed, @NotNull Boolean bleeding,
            @NotNull Boolean itchingOrPain, @NotNull Boolean notHealing,
            @NotNull Boolean personalHistory, @NotNull Boolean familyHistory) {}

    @PostMapping("/assessment")
    public PriorityService.Assessment assess(@Valid @RequestBody Request request) {
        return service.assess(new PriorityService.Questionnaire(request.changed(), request.bleeding(),
                request.itchingOrPain(), request.notHealing(), request.personalHistory(), request.familyHistory()));
    }
}
