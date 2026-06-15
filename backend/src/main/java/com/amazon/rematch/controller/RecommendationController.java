package com.amazon.rematch.controller;

import com.amazon.rematch.dto.*;
import com.amazon.rematch.service.RecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/recommendations")
public class RecommendationController {

    private final RecommendationService recommendationService;

    /** GET /recommendations/{userId} — active recommendations, highest score first */
    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<List<RecommendationResponse>>> getRecommendations(
            @PathVariable Long userId) {
        return ResponseEntity.ok(ApiResponse.ok(
                recommendationService.getRecommendationsForUser(userId)));
    }

    /** GET /recommendations/{userId}/nearby-products?top=10 */
    @GetMapping("/{userId}/nearby-products")
    public ResponseEntity<ApiResponse<List<RecommendationResponse>>> getNearbyProducts(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "10") int top) {
        return ResponseEntity.ok(ApiResponse.ok(
                recommendationService.getNearbyProductsForUser(userId, top)));
    }

    /** POST /recommendations/{userId}/generate */
    @PostMapping("/{userId}/generate")
    public ResponseEntity<ApiResponse<List<RecommendationResponse>>> generate(
            @PathVariable Long userId) {
        return ResponseEntity.ok(ApiResponse.ok(
                "Recommendations generated successfully.",
                recommendationService.generateRecommendations(userId)));
    }

    /** PATCH /recommendations/{id}/status — body: "ACTIVE" | "DISMISSED" | "PURCHASED" */
    @PatchMapping("/{id}/status")
    public ResponseEntity<ApiResponse<RecommendationResponse>> updateStatus(
            @PathVariable Long id,
            @RequestBody String status) {
        return ResponseEntity.ok(ApiResponse.ok(
                recommendationService.updateStatus(id, status.trim().replace("\"", ""))));
    }

    /**
     * GET /recommendations/nearby-users/{productId}?userId=<id>
     * userId passed as query param — no JWT needed.
     */
    @GetMapping("/nearby-users/{productId}")
    public ResponseEntity<ApiResponse<List<NearbyUserResponse>>> getNearbyUsers(
            @PathVariable Long productId,
            @RequestParam Long userId) {
        return ResponseEntity.ok(ApiResponse.ok(
                recommendationService.getNearbyUsers(productId, userId)));
    }

    /** POST /recommendations/browse?userId=&category= */
    @PostMapping("/browse")
    public ResponseEntity<ApiResponse<Void>> recordBrowse(
            @RequestParam Long userId,
            @RequestParam String category) {
        recommendationService.recordBrowse(userId, category);
        return ResponseEntity.ok(ApiResponse.ok(null));
    }

    /** POST /recommendations/purchase?userId=&category= */
    @PostMapping("/purchase")
    public ResponseEntity<ApiResponse<Void>> recordPurchase(
            @RequestParam Long userId,
            @RequestParam String category) {
        recommendationService.recordPurchase(userId, category);
        return ResponseEntity.ok(ApiResponse.ok(null));
    }

    /** GET /recommendations/{id}/explain */
    @GetMapping("/{id}/explain")
    public ResponseEntity<ApiResponse<BedrockExplanationResponse>> explain(
            @PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok(
                recommendationService.explainRecommendation(id)));
    }
}
