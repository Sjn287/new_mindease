package MindEase.demo.Controller;


import MindEase.demo.Model.Users;
import MindEase.demo.Repository.UserRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
@CrossOrigin(origins = "*")
public class UserController {
    private final UserRepository userRepository;
    public UserController(UserRepository userRepository){
        this.userRepository = userRepository;
    }
    @GetMapping
    public List<Users> getAllUsers(){
        return userRepository.findAll();
    }

    @PostMapping
    public Users createUser(@RequestBody Users user){
        return userRepository.save(user);
    }

}
