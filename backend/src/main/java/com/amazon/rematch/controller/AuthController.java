package com.amazon.rematch.controller;

import com.amazon.rematch.dto.AuthResponse;
import com.amazon.rematch.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserRepository userRepository;

    /**
     * GET /auth/users
     * Returns all demo users. Frontend shows these in a picker — no password needed.
     */
    @GetMapping("/users")
    public ResponseEntity<List<AuthResponse>> getUsers() {
        List<AuthResponse> users = userRepository.findAll().stream()
            .map(u -> AuthResponse.builder()
                .id(u.getId())
                .name(u.getName())
                .email(u.getEmail())
                .phone(u.getPhone())
                .city(u.getCity())
                .state(u.getState())
                .country(u.getCountry())
                .latitude(u.getLatitude())
                .longitude(u.getLongitude())
                .role(u.getRole().name())
                .build())
            .toList();
        return ResponseEntity.ok(users);
    }

    /**
     * GET /auth/users/{id}
     * Returns a single user by ID. Used on page load to rehydrate the session.
     */
    @GetMapping("/users/{id}")
    public ResponseEntity<AuthResponse> getUserById(@PathVariable Long id) {
        return userRepository.findById(id)
            .map(u -> ResponseEntity.ok(AuthResponse.builder()
                .id(u.getId())
                .name(u.getName())
                .email(u.getEmail())
                .phone(u.getPhone())
                .city(u.getCity())
                .state(u.getState())
                .country(u.getCountry())
                .latitude(u.getLatitude())
                .longitude(u.getLongitude())
                .role(u.getRole().name())
                .build()))
            .orElse(ResponseEntity.notFound().build());
    }
}
