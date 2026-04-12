package com.lanchas.guides.model;

import io.micronaut.data.annotation.GeneratedValue;
import io.micronaut.data.annotation.Id;
import io.micronaut.data.annotation.MappedEntity;
import io.micronaut.serde.annotation.Serdeable;

@Serdeable
@MappedEntity
public class Guide {

    @Id
    @GeneratedValue(GeneratedValue.Type.AUTO)
    private Long id;

    private String name;
    private String phone;
    private String zone;
    private Integer experience;
    private Boolean active;

    public Guide() {
    }

    public Guide(String name, String phone, String zone, Integer experience) {
        this.name = name;
        this.phone = phone;
        this.zone = zone;
        this.experience = experience;
        this.active = true;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getZone() { return zone; }
    public void setZone(String zone) { this.zone = zone; }

    public Integer getExperience() { return experience; }
    public void setExperience(Integer experience) { this.experience = experience; }

    public Boolean getActive() { return active; }
    public void setActive(Boolean active) { this.active = active; }
}
