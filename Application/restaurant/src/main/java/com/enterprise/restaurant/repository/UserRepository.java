package com.enterprise.restaurant.repository;

import com.enterprise.restaurant.dataobject.User;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Integer> {
  List<User> findByEmail(String email);

}
